from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from notifications.notification_funcs import NotificationFuncs

EMAIL = None


class NotificationList:
    def __init__(self, config=None):
        """
        takes attributes from NotificationsConfigurator's object and set them as global variables then deletes the
        object

        :param config: NotificationsConfigurator's object comes from NotificationsConfigurator's constructor
        """

        global EMAIL

        EMAIL = config.EMAIL

        del config

    @staticmethod
    def notify_users_about_x(trackers: list, param_1: str, param_2: str):
        """
        formats the notification pattern and notification details before sending to users in trackers list

        :param trackers: list of trackers
        :param param_1: first parameter for details
        :param param_2: second parameter for details
        :return: None
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "mail subject_x"
        email_title = "good news!"
        email_content = f"this email sent by notify_users_about_y function<br>given param_1: {param_1} and given " \
                        f"param_2: {param_1}"

        html = Template(EMAIL).safe_substitute(email_title=email_title, email_content=email_content)
        msg.attach(MIMEText(html, "html"))

        message_0 = f"the first of the given arguments: {param_1}\n"
        message_1 = f"the second of the given arguments: {param_2}\n\n"
        message_2 = "additional message to show that how \"variable-length argument list\" works"

        NotificationFuncs.send_notification(trackers, message_0, message_1, message_2, msg=msg)

    @staticmethod
    def notify_users_about_y(trackers: list, param_1: str, param_2: str):
        """
        formats the notification pattern and notification details before sending to users in trackers list

        :param trackers: list of trackers
        :param param_1: first parameter for details
        :param param_2: second parameter for details
        :return: None
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "mail subject_y"
        email_title = "bad news!"
        email_content = f"this email sent by notify_users_about_y function<br>given param_1: {param_1} and" \
                        f" given param_2: {param_1}"

        html = Template(EMAIL).safe_substitute(email_title=email_title, email_content=email_content)
        msg.attach(MIMEText(html, "html"))

        message = f"the first of the given arguments: {param_1}\nthe second of the given arguments: " \
                  f"{param_2}\n\nadditional message to show that how \"variable-length argument list\" works"

        NotificationFuncs.send_notification(trackers, message, msg=msg)

    @staticmethod
    def notify_users_about_z(trackers: list, *args: tuple):
        """
        formats the notification pattern and notification details before sending to users in trackers list

        :param trackers: list of trackers
        :param args: variable-length argument list for details
        :return: None
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "mail subject_z"
        email_title = "breaking news!"
        email_content = f"this email sent by notify_users_about_y function<br>given param_1: {args[0]} and given " \
                        f"param_2: {args[0]}"

        html = Template(EMAIL).safe_substitute(email_title=email_title, email_content=email_content)
        msg.attach(MIMEText(html, "html"))

        message_0 = f"the first of the given arguments: {args[0]}\n"
        message_1 = f"the second of the given arguments: {args[1]}\n\n"
        message_2 = "additional message to show that how \"variable-length argument list\" works"

        NotificationFuncs.send_notification(trackers, message_0, message_1, message_2, msg=msg)
