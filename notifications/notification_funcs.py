import smtplib
import requests

NOTIFICATIONS_FILE = "configs/notifications.conf"
BASE_URL = "https://api.telegram.org/bot"

API_TOKEN = None
FULL_URL = None
MAIL_SERVER = None
PORT_NUMBER = None
SENDER_MAIL = None
SENDER_PASSWORD = None
TRACKERS = {}


class NotificationFuncs:
    def __init__(self, config=None):
        """
        takes attributes from NotificationsConfigurator's object and set them as global variables then deletes the
        object

        :param config: NotificationsConfigurator's object comes from NotificationsConfigurator's constructor
        """

        global API_TOKEN
        global FULL_URL
        global MAIL_SERVER
        global PORT_NUMBER
        global SENDER_MAIL
        global SENDER_PASSWORD
        global TRACKERS

        print("all of the trackers will be passed to global variables from object")

        API_TOKEN = config.API_TOKEN
        FULL_URL = config.FULL_URL
        MAIL_SERVER = config.MAIL_SERVER
        PORT_NUMBER = config.PORT_NUMBER
        SENDER_MAIL = config.SENDER_MAIL
        SENDER_PASSWORD = config.SENDER_PASSWORD
        TRACKERS = config.TRACKERS

        print("all of the trackers were passed to global variables from object")

        del config

    @staticmethod
    def send_notification(trackers: list, *messages: tuple, msg=None):
        """
        sends messages and emails to each user in trackers list

        :param trackers: list of trackers
        :param messages: messages for send to telegram
        :param msg: "email.mime.multipart.MIMEMultipart" objects for send as email
        :return: None
        """

        receivers_email_addresses = []
        smtp_object = smtplib.SMTP(MAIL_SERVER, PORT_NUMBER)
        smtp_object.ehlo()
        smtp_object.starttls()
        smtp_object.login(SENDER_MAIL, SENDER_PASSWORD)
        msg["From"] = SENDER_MAIL

        for tracker in trackers:
            try:
                receivers_email_addresses.append(TRACKERS['userList'][tracker]['mailAddress'])
            except KeyError:
                print("user could not found")
                continue

            for message in messages:
                requests_string = f"{FULL_URL}sendMessage?chat_id=" \
                                  f"{TRACKERS['userList'][tracker]['telegramChatID']}&text={message}"
                try:
                    response = requests.get(requests_string)
                    if response.status_code == 200:
                        pass
                    else:
                        print("telegram message could not be sent, status code of response is", response.status)
                except Exception as e:
                    print("telegram message could not be sent:", e)

        msg["To"] = ", ".join(receivers_email_addresses)

        try:
            smtp_object.send_message(msg)
        except Exception as e:
            print("email could not be sent:", e)
        finally:
            smtp_object.quit()
