from notifications.notification_list import NotificationList
from notifications.notification_configurator import NotificationConfigurator

# it is better to call this constructor in your applications cli.py file or starting point of the your applications flow
NotificationConfigurator()

# usernames, comes from application flow
users = ["user_a", "user_b"]

# check "notification_list.py" for different notification methods
NotificationList.notify_users_about_x(users, "argument_a", "argument_b")

x = input("type anything to exit")
