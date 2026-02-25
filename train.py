import os
import time
import argparse

import torch

from tetris_env import TetrisEnv
from dqn_agent import DQNAgent


def train(args):
    env = TetrisEnv()
    agent = DQNAgent(
        device=args.device,
        lr=args.lr,
        gamma=args.gamma,
        buffer_size=args.buffer_size,
        batch_size=args.batch_size,
        epsilon_start=args.epsilon_start,
        epsilon_end=args.epsilon_end,
        epsilon_decay_steps=args.epsilon_decay_steps,
        target_update_freq=args.target_update_freq,
    )

    os.makedirs(args.model_dir, exist_ok=True)

    if args.resume:
        agent.load(args.resume)
        print(f"Resumed from {args.resume}")

    best_score = 0
    scores, lines_list, pieces_list = [], [], []
    start = time.time()

    for ep in range(1, args.episodes + 1):
        afterstates = env.reset()
        done = False
        pieces = 0
        info = {"score": 0, "lines": 0, "lines_cleared": 0}

        while not done:
            action, features = agent.select_action(afterstates)
            if action is None:
                break

            next_afterstates, reward, done, info = env.step(action)
            agent.store(features, reward, next_afterstates, done)
            agent.train_step()

            afterstates = next_afterstates
            pieces += 1

        scores.append(info["score"])
        lines_list.append(info["lines"])
        pieces_list.append(pieces)

        if info["score"] >= best_score:
            best_score = info["score"]
            agent.save(os.path.join(args.model_dir, "best_model.pth"))

        if ep % args.save_every == 0:
            agent.save(os.path.join(args.model_dir, f"checkpoint_{ep}.pth"))

        if ep % args.log_every == 0:
            n = min(args.log_every, len(scores))
            print(
                f"Ep {ep}/{args.episodes} | "
                f"Score {sum(scores[-n:]) / n:.1f} | "
                f"Lines {sum(lines_list[-n:]) / n:.1f} | "
                f"Pieces {sum(pieces_list[-n:]) / n:.1f} | "
                f"Best {best_score} | "
                f"Eps {agent.epsilon:.4f} | "
                f"{time.time() - start:.0f}s"
            )

    agent.save(os.path.join(args.model_dir, "final_model.pth"))
    print(f"\nDone. Best score: {best_score}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Train Tetris DQN Agent")
    p.add_argument("--episodes", type=int, default=10000)
    p.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
    )
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--gamma", type=float, default=0.99)
    p.add_argument("--buffer-size", type=int, default=30000)
    p.add_argument("--batch-size", type=int, default=512)
    p.add_argument("--epsilon-start", type=float, default=1.0)
    p.add_argument("--epsilon-end", type=float, default=0.001)
    p.add_argument("--epsilon-decay-steps", type=int, default=75000)
    p.add_argument("--target-update-freq", type=int, default=500)
    p.add_argument("--model-dir", type=str, default="models")
    p.add_argument("--save-every", type=int, default=1000)
    p.add_argument("--log-every", type=int, default=100)
    p.add_argument("--resume", type=str, default=None)
    train(p.parse_args())
