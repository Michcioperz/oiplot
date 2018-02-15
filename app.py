#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import time
import datetime

sessionid = ""

def fetch():
    r = requests.get("https://sio2.mimuw.edu.pl/c/oi25-2/workers/load.json", cookies=dict(sessionid=sessionid))
    r.raise_for_status()
    return r.json()

second = datetime.timedelta(seconds=1)
second10 = 10 * second

def create(data):
    X = range(-10, 1)
    Y = [data[u"capacity"]] * len(X)
    Z = [0] + [data[u"load"]] * (len(X) - 1)
    with plt.xkcd():
        t = plt.text(0, data[u"load"], str(data[u"load"]))
        t.set_color('y')
        t.set_ma('right')
        t.set_size(50)
        plt.title("Wczytaj")
        plt.xlabel("czas")
        plt.ylabel("sprawdzaczki")
        graph_capacity, = plt.plot(X, Y, 'b')
        graph_load, = plt.plot(X, Z, 'y')
        return (X, graph_capacity, Y, graph_load, Z, t)


def refresh(old, data):
    with plt.xkcd():
        X, cap, Y, load, Z, t = old
        Y = Y[1:]
        Z = Z[1:]
        Y += [data[u"capacity"]]
        Z += [data[u"load"]]
        t.set_text(str(data[u"load"]))
        t.set_y(data[u"load"])
        cap.set_ydata(Y)
        load.set_ydata(Z)
        plt.draw()
        return (X, cap, Y, load, Z, t)

graph = create(fetch())
plt.ion()
while True:
    plt.pause(0.01)
    graph = refresh(graph, fetch())
