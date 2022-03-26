# notifyingUsersSync
Notifying users via Telegram and email using Python.

Configure **/config/notifications.conf** file and implement your project easily.

Please make sure your Python version is newer or equal to 3.8. If your version is lower than 3.8, change **the walrus operator** which in **/notifications/notification_configurator.py** file with a standart if condition line;

```
if not (telegram_chat_id := self.get_chat_id(telegram_username)) is None:
``` 

change this line with;

```
if not self.get_chat_id(telegram_username) is None:
	telegram_chat_id = self.get_chat_id(telegram_username)
```

after this *notifyingUsersSync* can run with Python 3.7 or newer versions.