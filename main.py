import argparse
import os
from utils import Logger
from enviroment.board import Board

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
        type=int,
        default=10,
        help="Size of the board",
    )
    parser.add_argument(
        "-speed",
        type=int,
        default=100,
        help="Speed of the game",
    )
    return parser.parse_args()

def main():
    agrs = parse_args()
    logger = Logger()
    boar_size= agrs.board_size
    board = Board(boar_size, logger)

if __name__ == "__main__":
    main()
