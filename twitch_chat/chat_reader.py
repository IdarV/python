#! /usr/bin/env python3
class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


import socket
import yaml
import threading
from time import strftime


# Setup global vars
def setup():

    global HOST
    global PORT
    global CHANNEL
    global PASS
    global NICK

    with open("environment.yml", 'r') as stream:
        doc = yaml.load(stream)
        HOST = doc["HOST"]
        PORT = int(doc["PORT"])
        CHANNEL = doc["CHANNEL"]
        PASS = doc["PASS"]
        NICK = doc["NICK"]


# checks for answer trigger. we will respond if triggered #tumblr
def answer_trigger(message):
    return "!norway" == message[1:].strip()


# prints message to console. "sender : message"
def print_message(sender, message, color):
    print(color + sender + " : " + message[1:] + Bcolors.ENDC)


# sends a IRC PRIVMSG to the socket
def send_message(_socket, message):
    _socket.send(bytes("PRIVMSG " + CHANNEL + " :" + message + "\n", "UTF-8"))


# pulls the sender's name from header
def get_sender_name(header):
    sender = ""
    for char in header:
                    if char == "!":
                        break
                    if char != ":":
                        sender += char
    return sender


# simple lambda to change between colors
def change_color(color):
    return Bcolors.WARNING if color == Bcolors.OKGREEN else Bcolors.OKGREEN


# returns sub-string between first and last strings
def find_between(sting, first, last):
    try:
        start = sting.index(first) + len(first)
        end = sting.index(last, start)
        return sting[start:end]
    except ValueError:
        return ""


# tries to connect to and run the chat
def run_chat():
    color = Bcolors.OKGREEN
    readbuffer = ""
    print("#Connecting to " + HOST + ":" + str(PORT))
    s = socket.socket()
    print(HOST, str(PORT))
    s.connect((HOST, PORT))
    print("#Connected to " + HOST + ":" + str(PORT))

    s.send(bytes("PASS %s\r\n" % PASS, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("JOIN %s\r\n" % CHANNEL, "UTF-8"))

    while 1:
        readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
        incoming_msg = str.split(readbuffer, "\n")
        readbuffer = incoming_msg.pop()

        for line in incoming_msg:
            line = str.rstrip(line)
            line = str.split(line)

            if line[0] == "PING":
                s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
            if line[1] == "PRIVMSG":
                sender = get_sender_name(line[0])

                size = len(line)
                i = 3
                message = ""
                while i < size:
                    message += line[i] + " "
                    i += 1
                print_message(sender, message, color)

                if answer_trigger(message):
                    print("# FOUND TRIGGER, RESPONDING")
                    send_message(s, "Time in Norway: %s" % strftime("%H:%M:%S"))
                color = change_color(color)


# main
def main():
    try:
        threading.Thread(target=run_chat()).start().join()
    except:
        print('Error: unable to start thread')


# PROGRAM START#
setup()
main()
