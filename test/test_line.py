from line_notify import LineNotify

import os
from dotenv import load_dotenv
load_dotenv()

LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

line_notify = LineNotify(LINE_NOTIFY_TOKEN)
line_notify.send("Hello World")
