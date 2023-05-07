from line_notify import LineNotify

LINE_NOTIFY_TOKEN = "MiGiGvEehvIskk3qJrXLFeQ78Adpf9UvLO2wGLgA9JP"
line_notify = LineNotify(LINE_NOTIFY_TOKEN)
line_notify.send("Hello World")
