import argparse
import os
from utils.logger import Logger
from enviroment.board import Board
from enviroment.gui import GUI
from agent.q_agent import QAgent


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
        default=1,
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
    logger = Logger()
    board_size = args.board_size
    board = Board(board_size, logger)
    agent = QAgent(board_size, logger)

    if args.load:
        if os.path.exists(args.load):
            logger.log(f"Loading model from {args.load}")
            agent.load(args.load)
        else:
            logger.log(f"Error: Model file {args.load} not found")
            return

    gui = None
    if args.visual == "on":
        gui = GUI(board, args.speed)

        while True:
            gui.update()


if __name__ == "__main__":
    main()
