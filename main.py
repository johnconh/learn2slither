import argparse
import os
from agent import Agent
from snakeAI import Snake
from plot import plot
from config_panel import launch_config_panel
import pygame
import matplotlib.pyplot as plt


def pth_file(value):
    """
    Custom type for file paths.
    """
    if not value.endswith('.pth'):
        raise argparse.ArgumentTypeError(
            f"Invalid file name: {value}. Must end with .pth"
        )
    return value


def positive_int(value):
    """
    Custom type for positive integers.
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    if ivalue > 1000:
        raise argparse.ArgumentTypeError(f"{value} is too large. Max is 1000")
    return ivalue


def board_size_type(value):
    """
    Custom type for board size.
    """
    ivalue = int(value)
    if ivalue < 7 or ivalue > 42:
        raise argparse.ArgumentTypeError(f"{value} is not a valid board size")
    return ivalue


def parse_args():
    parser = argparse.ArgumentParser(description="Learn2Slither")
    parser.add_argument(
        "-sessions",
        type=positive_int,
        default=10,
        help="Number training session",
    )
    parser.add_argument(
        "-visual",
        type=str,
        choices=["on", "off"],
        default='on',
        help="Enables or disables the visualisation of the game",
    )
    parser.add_argument(
        "-save",
        type=pth_file,
        default=None,
        help="Path to save the trainer model. ",
    )
    parser.add_argument(
        "-load",
        type=str,
        default=None,
        help="Path to load the trainer model",
    )
    parser.add_argument(
        "-dontlearn",
        action="store_true",
        help="Disables the learning process",
    )
    parser.add_argument(
        "-step-by-step",
        action="store_true",
        help="Enables step-by-step mode",
    )
    parser.add_argument(
        "-board-size",
        type=board_size_type,
        default=10,
        help="Size of the board",
    )
    parser.add_argument(
        "-speed",
        type=positive_int,
        default=100,
        help="Speed of the game",
    )
    parser.add_argument(
        "-game",
        action="store_true",
        help="Launch GUI configuration panel",
    )
    return parser.parse_args()


def run_game(args):
    game = Snake(args.board_size, args.visual, args.step_by_step, args.speed)
    agent = Agent()
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    session = args.sessions

    if args.load:
        if os.path.exists(args.load):
            agent.model.load(args.load)
            agent.epsilon = -1000
        else:
            print(f"Model file {args.load} not found.")
            return
    try:
        while session > 0:
            state_old = game.get_state()
            final_move = agent.get_action(
                state_old, args.sessions, args.dontlearn)
            reward, done, score = game.play_step(final_move)
            state_new = game.get_state()

            if not args.dontlearn:
                agent.train_short_memory(
                    state_old, final_move, reward, state_new, done)
                agent.remember(state_old, final_move, reward, state_new, done)
            if done:
                session -= 1
                game.reset()
                agent.n_games += 1

                if not args.dontlearn:
                    agent.train_long_memory()

                if score > record:
                    record = score

                if args.save:
                    agent.model.save(args.save)

                print('Game', agent.n_games, 'Score', score, 'Record:', record)

                if not args.dontlearn:
                    plot_scores.append(score)
                    total_score += score
                    mean_score = total_score / agent.n_games
                    plot_mean_scores.append(mean_score)
                    plot(plot_scores, plot_mean_scores)
    finally:
        pygame.quit()
        plt.close('all')


def main():
    args = parse_args()

    if args.game:
        launch_config_panel(run_game, args)
        return
    else:
        run_game(args)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
