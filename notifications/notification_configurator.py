import os
import json
import requests
from config import Config
from notifications.notification_list import NotificationList
from notifications.notification_funcs import NotificationFuncs

NOTIFICATIONS_FILE = "configs/notifications.conf"
BASE_URL = "https://api.telegram.org/bot"


class NotificationConfigurator:
    def __init__(self):
        """
        assigns notification settings to attributes then checks if 'notificationsConfig.json' file exists; if the
        file exists, it appends new user, if not creates new file and append the user details into this
        """

        self.EMAIL = None
        self.TRACKERS = None
        self.MAIL_SERVER = None
        self.PORT_NUMBER = None
        self.SENDER_MAIL = None
        self.SENDER_PASSWORD = None

        try:
            self.notifications_config = Config(NOTIFICATIONS_FILE).get("NOTIFICATIONS")
        except Exception as e:
            print(e)

        self.BOT_UID = self.notifications_config["TELEGRAM"]["BOT_UID"]
        self.API_TOKEN = self.notifications_config["TELEGRAM"]["API_TOKEN"]
        self.FULL_URL = BASE_URL + self.API_TOKEN + "/"

        print("notifications configurator started")

        if not os.path.exists("configs/notificationsConfig.json"):
            print("no 'notificationsConfig.json' config found at 'configs/', creating now")

            raw_dict = {"userList": {}}
            dict_type_object_of_json = self.add_user(raw_dict)

            try:
                with open("configs/notificationsConfig.json", "w") as file:
                    file.write(dict_type_object_of_json)
            except Exception as e:
                print("'config/notificationsConfig.json' could not configured:", e)

        else:
            selection = "-"

            while not (selection == "" or selection == "exit"):
                selection = input("press enter to add new user or type \"exit\" to exit adding section\n")

                if selection == "":
                    try:
                        with open("configs/notificationsConfig.json", encoding='utf-8') as file:
                            raw_dict = json.load(file)
                    except Exception as e:
                        print("'config/notificationsConfig.json' could not configured:", e)

                    dict_type_object_of_json = self.add_user(raw_dict)

                    try:
                        with open("configs/notificationsConfig.json", "w") as file:
                            file.write(dict_type_object_of_json)
                    except Exception as e:
                        print("'config/notificationsConfig.json' could not configured:", e)
                    break

                elif selection == "exit":
                    print("moving to main workflow")
                    break

                else:
                    print("please press enter or type \"exit\"")

        self.get_entire_config()

        print("notifications configurator completed")

        NotificationFuncs(self)
        NotificationList(self)

    def add_user(self, raw_dict: dict):
        """
        appends new user to "notificationConfig.json" file then saves

        :param raw_dict: existing "notificationConfig.json" file in dict type
        :return: updated "notificationConfig.json" file in dict type
        """

        message = "configuration complete"

        while True:
            username = input("user: ")
            mail_address = input("email: ")
            telegram_username = input("telegram_uid: ")

            if not (telegram_chat_id := self.get_chat_id(telegram_username)) is None:
            # if not self.get_chat_id(telegram_username) is None:
            #     telegram_chat_id = self.get_chat_id(telegram_username)
                try:
                    requests_string = f"{self.FULL_URL}sendMessage?chat_id={telegram_chat_id}&text={message}"

                    if requests.get(requests_string).status_code == 200:
                        print(f"configuration successful - (chat_id: {telegram_chat_id}).")

                    else:
                        print("configuration failed, try again")
                        continue
                except Exception as e:
                    print("Hata:", e)

            else:
                print(
                    f"the user \"{username}\" with telegram_uid \"{telegram_username}\" does not seem like interacted "
                    f"with \"{self.BOT_UID}\" by typing \"/start\"")
                continue

            raw_dict["userList"][username] = {"mailAddress": f"{mail_address}",
                                              "telegramUsername": f"{telegram_username}",
                                              "telegramChatID": f"{telegram_chat_id}"}
            dict_type_object_of_json = json.dumps(raw_dict)

            another_one = input("press enter to add another user or type \"exit\" to exit adding section")

            if another_one == "exit":
                break

            else:
                continue

        return dict_type_object_of_json

    def get_chat_id(self, username: str):
        """
        scans messages on telegram-api from last to first then returns chat id of the user if the user typed "/start"
        before

        :param username: telegram username
        :return: chat id between bot and user in int type
        """

        response = requests.get(f"{self.FULL_URL}getUpdates")
        for update in response.json()["result"][::-1]:
            if "message" in update:
                if update["message"]["text"] == "/start":
                    if update["message"]["from"]["username"] == username:
                        return update["message"]["from"]["id"]

            else:
                return False

    def get_entire_config(self):
        """
        assigns updated file which named as "notificationConfig.json" to "self" object

        :return: None
        """

        self.MAIL_SERVER = self.notifications_config["MAIL"]["MAIL_SERVER"]
        self.PORT_NUMBER = self.notifications_config["MAIL"]["PORT"]
        self.SENDER_MAIL = self.notifications_config["MAIL"]["SENDER_MAIL"]
        self.SENDER_PASSWORD = self.notifications_config["MAIL"]["SENDER_PASSWORD"]

        try:
            with open("configs/notificationsConfig.json", encoding='utf-8') as file:
                self.TRACKERS = json.load(file)
        except Exception as e:
            print("'config/notificationsConfig.json' could not configured:", e)

        try:
            with open('notifications/email.html', encoding='utf-8') as email:
                self.EMAIL = email.read()
        except Exception as e:
            print("'notifications/email.html' could not configured:", e)
