import subprocess
import shlex
import time
from collections import deque
from copy import deepcopy


#for line in iter(proc.stdout.readline, ""):
#    print line,


class Background():
    def __init__(self, command, parser):
        self.proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        self.parser = parser

    def run(self, conn):
        for line in iter(self.proc.stdout.readline, ""):
            self.parser.parse_line(line)
            if conn.poll():
                rec = conn.recv()
                conn.send(listify_deques(deepcopy(self.parser.data)))


def listify_deques(data):
    for k,v in data.items():
        if isinstance(v, deque):
            data[k] = list(v)
        elif isinstance(v, dict):
            listify_deques(v)
    return data
