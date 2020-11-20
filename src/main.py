import os
import time
from dotenv import load_dotenv
from argument_parser import ArgumentParser
from utils import Utils
from client import Client
from message import Message
from slack_bot import SlackBot

NUM_ITER = 4


def main():
    Utils.print_log("start bot")

    load_dotenv()
    argument_parser = ArgumentParser()

    snkrs_pass_urls = Client.request()

    if len(snkrs_pass_urls) > 0:
        slack_bot = SlackBot(
            os.environ["CHANNEL"], os.environ["TEST_CHANNEL"], os.environ["SLACK_API_TOKEN"])
        for url in snkrs_pass_urls:
            message = Message.make_message(url)
            slack_bot.post_message(
                message,
                is_test=argument_parser.arguments.test
            )

    Utils.print_log("stop bot")


if __name__ == "__main__":
    for _ in range(NUM_ITER):
        main()
        time.sleep(5)
