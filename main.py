import argparse
import os
import time

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
            agent.load_model(args.load)
        else:
            logger.log(f"Error: Model file {args.load} not found")
            return

    gui = None
    if args.visual == "on":
        gui = GUI(board, args.speed)

    max_lenth = 0
    max_steps = 0
    sesision_stats = []
    total_apples = 0

    for session in range(args.sessions):
        board.reset()
        done = False
        steps = 0
        start_time = time.time()
        session_apples = 0

        while not done:
            state = board.get_snake_vision()
            current_dir = board.direction
            action = agent.choose_action(state, current_dir)
            reward, done, info = board.step(action)
            next_state = board.get_snake_vision()
            board.print_snake_vision_grid()

            if info.get("reason") == "Ate green apple":
                session_apples += 1
                total_apples += 1

            if not args.dontlearn:
                agent.update(state, action, reward, next_state, done)

            if gui:
                gui.update()
                if args.step_by_step:
                    gui.wait_for_key()

            steps += 1
            if board.snake_length > max_lenth:
                max_lenth = board.snake_length
    
            if args.visual.lower() == "off":
                logger.log(f"Session {session+1}, Step {steps}, Snake length: {board.snake_length}")
                logger.log(f"Action: {action}, Reward: {reward}, Info: {info}")
                logger.log(f"Exploration rate: {agent.exploration_rate:.4f}")
        sesion_duration = time.time() - start_time
        sesision_stats.append({
            "session": session + 1,
            "duration": sesion_duration,
            "apples": session_apples,
            "steps": steps,
            "snake_length": board.snake_length
        })
        if steps > max_steps:
            max_steps = steps

        logger.log(f"Session {session+1}/{args.sessions}")
        logger.log(f"Length: {board.snake_length}, Steps: {steps}")
        logger.log(f"Duration: {sesion_duration:.2f}s, Apples: {session_apples}")

    if args.save and not args.dontlearn:
        save_dir = os.path.dirname(args.save)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        agent.save_model(args.save)
        logger.log(f"Save learning state in {args.save}")

    logger.log(f"GAME   OVER")
    logger.log(f"Max length: {max_lenth}, Max steps: {max_steps}")
    logger.log(f"Total apples: {total_apples}")


if __name__ == "__main__":
    main()
