from saron.parse_sar import SARParser


hosts = ["localhost"]
commands = [("sar -dp -n DEV  -u 1", SARParser)]
