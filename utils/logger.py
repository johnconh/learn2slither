import time
import sys


class Logger:
    """
    Logger class for the snake game.
    Handles logging to console and optionally to a file.
    """
    def __init__(self, log_file=None, verbose=True):
        """
        Initialize the logger with optional file output.

        Args:
            log_file: Path to the log file (None for no file logging)
            verbose: If True, logs to console, otherwise silent
        """
        self.verbose = verbose
        self.log_file = log_file
        self.file = None
        if log_file:
            try:
                self.file = open(log_file, 'w')
            except Exception as e:
                print(f"Error opening log file {log_file}: {e}")
                self.file = None

    def log(self, message):
        """
        Log a message to console and file if applicable.

        Args:
            message: The message to log
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_msg = f"[{timestamp}] {message}"

        if self.verbose:
            print(log_msg)
            sys.stdout.flush()
        if self.file:
            try:
                self.file.write(log_msg + '\n')
                self.file.flush()
            except Exception as e:
                print(f"Error writing to log file: {e}")

    def close(self):
        """
        Close the log file if it was opened.
        """
        if self.file:
            try:
                self.file.close()
            except Exception as e:
                print(f"Error closing log file: {e}")
        self.file = None

    def __del__(self):
        """
        Destructor to ensure the log file is closed.
        """
        self.close()
