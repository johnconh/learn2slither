import argparse
import os
from agent import Agent
from snakeAI import Snake
from plot import plot


def positive_int(value):
    """
    Custom type for positive integers.
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue


def board_size_type(value):
    """
    Custom type for board size.
    """
    ivalue = int(value)
    if ivalue < 10 or ivalue > 42:
        raise argparse.ArgumentTypeError(f"{value} is not a valid board size")
    return ivalue


def parse_args():
    parser = argparse.ArgumentParser(description="Learn2Slither")
    parser.add_argument(
        "-sessions",
        type=int,
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
        type=str,
        default=None,
        help="Path to save the trainer model",
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
    return parser.parse_args()


def main():
    args = parse_args()
    game = Snake(args.board_size, args.visual, args.step_by_step, args.speed)
    agent = Agent()
    plot_scores = []  
    plot_mean_scores = []
    total_score = 0
    record = 0
    session = args.sessions

    while session > 0:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        if not args.dontlearn:
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            agent.remenber(state_old, final_move, reward, state_new, done)
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

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    main()
