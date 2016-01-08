#!/usr/bin/env python3

# Standard packages
import logging
import threading
import requests
import json
import shlex
import subprocess
# Local packages
import recording
import playwav

running = True
skip = False

def main():
    say("ready")
    global skip
    while running:
        if skip or recording.passive_listen():
            threading.Thread(None, playwav.playwav, "readySound", ["data/ding.wav"]).start()
            message = recording.active_listen()
            if message:
                interpret_command(message)
                skip=False
            else:
                say("Excuse me, what did you say?")
                skip=True

def interpret_command(fullcommand):
    global running
    global skip
    if fullcommand == "quit":
        running = False
        say("Bye bye")
        return
    command = fullcommand.split(' ')
    if command[0] == "lights" or command[0] == "light" or command[0] == "lamp" or command[0] == "lamps":
        data = {"id": "lightbtn1",
                "type": "button",
                "data":{"action": "pressed"}}
        send_message(data)
    elif command[0] == "abort":
        pass
    else:
        say("Sorry, couldn't interpret your request")

def send_message(msg):
    try:
        jsn = json.dumps(msg)
        requests.request("POST", "http://127.0.0.1:5600/api/v0/event", json=jsn)
    except Exception as e:
        print(e)
        say("Couldn't connect to homebrain server")

def say(msg, wait=True):
    print("Saying: " + msg)
    command = shlex.split("espeak \"{}\"".format(msg))
    if wait:
        subprocess.call(command)
    else:
        subprocess.Popen(command)

if __name__ == "__main__":
    main()
