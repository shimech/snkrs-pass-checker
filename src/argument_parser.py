import argparse


class ArgumentParser:
    def __init__(self):
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument(
            "-t", "--test", action="store_true", help="post a message to test channel"
        )
        self.arguments = argument_parser.parse_args()
