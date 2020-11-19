import datetime


class Utils:
    @staticmethod
    def get_datetime_now():
        return datetime.datetime.now()

    @classmethod
    def print_log(cls, description):
        print("[{}] {}".format(cls.get_datetime_now(), description))
