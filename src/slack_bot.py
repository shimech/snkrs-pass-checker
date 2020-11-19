from slacker import Slacker
from utils import Utils


class SlackBot:
    def __init__(self, channel, test_channel, slack_api_token):
        self.slacker = Slacker(slack_api_token)
        self.channel = channel
        self.test_channel = test_channel

    def post_message(self, message, is_test=False):
        channel = self.test_channel if is_test else self.channel
        try:
            self.slacker.chat.post_message(channel, message)
            Utils.print_log("post message to {}".format(channel))
        except:
            Utils.print_log("FAIL to post message to {}".format(channel))
