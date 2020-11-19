class Message:
    snkrs_pass_message = "<!channel> 【SNKRS PASS Flying Get!!!】" + "\n"
    snkrs_pass_message += "SNKRS PASSが発行されました！急げ！！:snkrspass:" + "\n"
    snkrs_pass_message += "{}" + "\n"

    @classmethod
    def make_message(cls, url):
        return cls.snkrs_pass_message.format(url)
