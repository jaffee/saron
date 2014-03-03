import re
import time
from collections import deque


class SARParser():
    def __init__(self, maxlen=50):
        self.headers = None
        self.data = {}
        self.maxlen = maxlen

    # { subj: {metric: [[ts, val], [ts, val]]}}
    def parse_line(self, line):
        if not re.search("^\d", line):
            return
        s = line.split()
        if re.search("^[A-Z]*$", s[2]):
            self.headers = s
            return
        subject = self.headers[2] + "_" + s[2]
        for i,value in enumerate(s):
            if i < 3:
                continue
            metric = self.headers[i]
            self.data.setdefault(subject,
                                 {}).setdefault(metric,
                                                deque(maxlen=self.maxlen)).append([int(time.time()),
                                                                                     float(value)])



# def parse_sar(text, ret=None):
#     headers = None
#     if not ret:
#         ret = {}
#     for line in text.split("\n"):
#         if not re.search("^\d", line):
#             continue
#         s = line.split()
#         if re.search("^[A-Z]*$", s[2]):
#             headers = s
#             continue
#         subject = headers[2] + "_" + s[2]
#         for i,value in enumerate(s):
#             if i < 3:
#                 continue
#             metric = headers[i]
#             metric = metric.replace("%", "pcnt")
#             metric = metric.replace("/", "_per_")
#             ret.setdefault(subject, {}).setdefault(metric, []).append([convert_time(s[0]), float(value)])
#     return ret


# def test_parse_sar():
#     text = """Linux 3.13-1-amd64 (cliffhanger)        02/23/2014      _x86_64_        (8 CPU)

# 10:44:16 PM       DEV       tps  rd_sec/s  wr_sec/s  avgrq-sz  avgqu-sz     await     svctm     %util
# 10:44:17 PM       sda      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
# 10:44:17 PM       sdb      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
# 10:44:17 PM       sdc      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00

# Average:          DEV       tps  rd_sec/s  wr_sec/s  avgrq-sz  avgqu-sz     await     svctm     %util
# Average:          sda      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
# Average:          sdb      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
# Average:          sdc      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00"""
#     ret = parse_sar(text)
#     expected = { "DEV_sda": {"tps": [["10:44:17", "0.00"]],
#                              "rd_sec/s": [["10:44:17", "0.00"]],
#                              "wr_sec/s": [["10:44:17", "0.00"]],
#                              "avgrq-sz": [["10:44:17", "0.00"]],
#                              "avgqu-sz": [["10:44:17", "0.00"]],
#                              "await": [["10:44:17", "0.00"]],
#                              "svctm": [["10:44:17", "0.00"]],
#                              "%util": [["10:44:17", "0.00"]]},
#                  "DEV_sdb": {"tps": [["10:44:17", "0.00"]],
#                              "rd_sec/s": [["10:44:17", "0.00"]],
#                              "wr_sec/s": [["10:44:17", "0.00"]],
#                              "avgrq-sz": [["10:44:17", "0.00"]],
#                              "avgqu-sz": [["10:44:17", "0.00"]],
#                              "await": [["10:44:17", "0.00"]],
#                              "svctm": [["10:44:17", "0.00"]],
#                              "%util": [["10:44:17", "0.00"]]},
#                  "DEV_sdc": {"tps": [["10:44:17", "0.00"]],
#                              "rd_sec/s": [["10:44:17", "0.00"]],
#                              "wr_sec/s": [["10:44:17", "0.00"]],
#                              "avgrq-sz": [["10:44:17", "0.00"]],
#                              "avgqu-sz": [["10:44:17", "0.00"]],
#                              "await": [["10:44:17", "0.00"]],
#                              "svctm": [["10:44:17", "0.00"]],
#                              "%util": [["10:44:17", "0.00"]]}}
#     assert ret == expected
