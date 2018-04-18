import os
import datetime
import copy
from webapp.models import LogModel


class LogHandler():

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        self.candidate_msg = []
        self.message_queue = []
        self.log_file = None

    def log(self, user, place, message):
        msg = {"user":user,
               "place":place,
               "msg":message,
               "time":datetime.datetime.now().strftime("%H:%M:%S")}
        self.candidate_msg.append(msg)
        self.write_msgs()

    def write_msgs(self):
        file_name = datetime.datetime.now().strftime("%Y_%m_%d") + ".csv"
        if (not self.log_file) or self.log_file.closed:
            self.log_file = open("logs/" + file_name, "a")
            if os.stat("logs/" + file_name).st_size == 0:
                self.log_file.write("ЧАС;КОРИСТУВАЧ;МІСЦЕ;ПОВІДОМЛЕННЯ\n")
        for msg in self.message_queue:
            self.log_file.write("{};{};{};{}\n".format(msg.get("time"),
                                                             msg.get("user"),
                                                             msg.get("place"),
                                                             msg.get("msg")))
        self.message_queue = []
        if self.candidate_msg:
            self.message_queue = copy.deepcopy(self.candidate_msg)
            self.candidate_msg = []
            self.log_file.close()
            self.write_msgs()
        else:
            self.log_file.close()

def write_log(user="-", place="-", msg_type="-", message="-"):
    try:
        new_log_obj = LogModel(date_added=datetime.datetime.now(),
                               user_id=user,
                               msg_source=place,
                               msg_type=msg_type,
                               msg=message)
        new_log_obj.save()
        # logger = LogHandler()
        # logger.log(user, place, message)
    except BaseException as e:
        print("Logger FAIL", str(e))