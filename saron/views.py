from saron import app
from flask import render_template, redirect, url_for
from saron.background import Background
from multiprocessing import Process, Pipe
import json
import signal
import sys
import time
from saron.commands import commands, hosts

processes, connections, backgrounds = {}, {}, {}


def mkssh(host, comm):
    return "ssh " + host + " '" + comm + "'"

for host in hosts:
    for comm in commands:
        backgrounds.setdefault(host, {})[comm] = Background(mkssh(host, comm[0]), comm[1]())
        p, c = Pipe()
        connections.setdefault(host, {})[comm] = p
        proc = Process(target=backgrounds[host][comm].run, args=(c,))
        processes.setdefault(host, {})[comm] = proc
        proc.start()


# b = Background("sar -dp 1", SARParser())
# parent_conn, child_conn = Pipe()
# p = Process(target=b.run, args=(child_conn,))
# p.start()

def signal_handler(signal, frame):
    for host in hosts:
        map(lambda b: b.proc.terminate(), backgrounds[host].values())
        map(lambda p: p.terminate(), processes[host].values())
    print("killin it!")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



@app.route('/')
def index():
    return redirect(url_for('dynamic'))
    # data = {}
    # for host in connections:
    #     hostdata = {}
    #     for comm, conn in connections[host].items():
    #         conn.send("gimme")
    #         hostdata.update(conn.recv())
    #     data[host] = hostdata
    # return render_template("main.html", data=data)

@app.route('/dynamic')
def dynamic():
    return render_template("dynamic.html")

@app.route('/data')
def raw_data():
    data = {}
    for host in connections:
        hostdata = {}
        for comm, conn in connections[host].items():
            conn.send("gimme")
            hostdata.update(conn.recv())
        data[host] = hostdata
    return json.dumps(data)
