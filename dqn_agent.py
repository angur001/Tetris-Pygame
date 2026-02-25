import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

NUM_FEATURES = 4
MAX_AFTERSTATES = 40


class ValueNetwork(nn.Module):
    def __init__(self, input_size=NUM_FEATURES):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, features, reward, next_features_pad, next_mask, done):
        self.buffer.append((features, reward, next_features_pad, next_mask, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        feats, rewards, nf, nm, dones = zip(*batch)
        return (
            np.array(feats),
            np.array(rewards, dtype=np.float32),
            np.array(nf),
            np.array(nm),
            np.array(dones, dtype=np.float32),
        )

    def __len__(self):
        return len(self.buffer)


class DQNAgent:
    def __init__(
        self,
        device="cpu",
        lr=1e-3,
        gamma=0.99,
        buffer_size=30_000,
        batch_size=512,
        epsilon_start=1.0,
        epsilon_end=0.001,
        epsilon_decay_steps=75_000,
        target_update_freq=500,
    ):
        self.device = torch.device(device)
        self.gamma = gamma
        self.batch_size = batch_size
        self.target_update_freq = target_update_freq

        self.value_net = ValueNetwork().to(self.device)
        self.target_net = ValueNetwork().to(self.device)
        self.target_net.load_state_dict(self.value_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.value_net.parameters(), lr=lr)
        self.buffer = ReplayBuffer(buffer_size)

        self.epsilon = epsilon_start
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay_steps = epsilon_decay_steps
        self.steps_done = 0

    # ------------------------------------------------------------------
    # Action selection
    # ------------------------------------------------------------------

    def select_action(self, afterstates):
        """Pick the best placement from [(action_idx, features), ...].
        Returns (action_idx, features) or (None, None) if empty.
        """
        if not afterstates:
            return None, None

        if random.random() < self.epsilon:
            idx = random.randrange(len(afterstates))
            return afterstates[idx]

        features = np.array([f for _, f in afterstates])
        with torch.no_grad():
            vals = self.value_net(torch.FloatTensor(features).to(self.device))
        best = vals.argmax().item()
        return afterstates[best]

    # ------------------------------------------------------------------
    # Replay buffer helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _pack_afterstates(afterstates):
        feats = np.zeros((MAX_AFTERSTATES, NUM_FEATURES), dtype=np.float32)
        mask = np.zeros(MAX_AFTERSTATES, dtype=bool)
        for i, (_, f) in enumerate(afterstates):
            feats[i] = f
            mask[i] = True
        return feats, mask

    def store(self, chosen_features, reward, next_afterstates, done):
        nf, nm = self._pack_afterstates(next_afterstates if not done else [])
        self.buffer.push(chosen_features, reward, nf, nm, done)

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    def train_step(self):
        if len(self.buffer) < self.batch_size:
            return None

        feats, rewards, nf, nm, dones = self.buffer.sample(self.batch_size)

        f = torch.FloatTensor(feats).to(self.device)          # [B, 4]
        r = torch.FloatTensor(rewards).to(self.device)         # [B]
        nf_t = torch.FloatTensor(nf).to(self.device)           # [B, 40, 4]
        nm_t = torch.BoolTensor(nm).to(self.device)            # [B, 40]
        d = torch.FloatTensor(dones).to(self.device)           # [B]

        predicted = self.value_net(f)                          # [B]

        with torch.no_grad():
            B = nf_t.shape[0]
            flat = nf_t.view(B * MAX_AFTERSTATES, NUM_FEATURES)
            flat_vals = self.target_net(flat).view(B, MAX_AFTERSTATES)
            flat_vals[~nm_t] = float("-inf")
            best_next = flat_vals.max(dim=1)[0]
            best_next = torch.where(d.bool(), torch.zeros_like(best_next), best_next)
            target = r + self.gamma * best_next

        loss = nn.MSELoss()(predicted, target)
        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.value_net.parameters(), 1.0)
        self.optimizer.step()

        self.steps_done += 1
        self.epsilon = max(
            self.epsilon_end,
            self.epsilon_start
            - (self.epsilon_start - self.epsilon_end)
            * self.steps_done
            / self.epsilon_decay_steps,
        )
        if self.steps_done % self.target_update_freq == 0:
            self.target_net.load_state_dict(self.value_net.state_dict())

        return loss.item()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path):
        torch.save(
            {
                "value_net": self.value_net.state_dict(),
                "target_net": self.target_net.state_dict(),
                "optimizer": self.optimizer.state_dict(),
                "steps_done": self.steps_done,
                "epsilon": self.epsilon,
            },
            path,
        )

    def load(self, path):
        ckpt = torch.load(path, map_location=self.device, weights_only=False)
        self.value_net.load_state_dict(ckpt["value_net"])
        self.target_net.load_state_dict(ckpt["target_net"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        self.steps_done = ckpt["steps_done"]
        self.epsilon = ckpt["epsilon"]
