import argparse

import pygame

from displays import Displays
from dqn_agent import DQNAgent
from tetris_env import TetrisEnv


def play(args):
    pygame.init()
    displays = Displays()
    screen = pygame.display.set_mode((Displays.SCREEN_W, Displays.SCREEN_H))
    pygame.display.set_caption("Tetris - AI Player")

    agent = DQNAgent()
    agent.load(args.model)
    agent.epsilon = 0.0

    env = TetrisEnv()
    afterstates = env.reset()

    clock = pygame.time.Clock()
    done = False
    running = True
    pieces_placed = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not done and running:
            action, _ = agent.select_action(afterstates)
            if action is not None:
                afterstates, _, done, info = env.step(action)
                pieces_placed += 1

        screen.fill((255, 255, 255))
        displays.drawFrame(screen, env.game)

        ai_font = pygame.font.Font(None, 28)
        ai_text = ai_font.render(
            f"AI  |  Pieces: {pieces_placed}", True, (0, 100, 200)
        )
        screen.blit(ai_text, (10, 80))

        if done:
            displays.DisplayGameOver(screen, env.game.score)

        pygame.display.flip()
        clock.tick(args.fps)

    pygame.quit()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Watch trained AI play Tetris")
    p.add_argument("--model", type=str, default="models/best_model.pth")
    p.add_argument("--fps", type=int, default=5)
    play(p.parse_args())
