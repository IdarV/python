#! /usr/bin/env python3


import socket
import yaml


def find_between(sting, first, last):
    try:
        start = sting.index(first) + len(first)
        end = sting.index(last, start)
        return sting[start:end]
    except ValueError:
        return ""


def setup():

    global HOST
    global PORT
    global PASS
    global NICK

    with open("environment.yml", 'r') as stream:
        doc = yaml.load(stream)
        HOST = doc["HOST"]
        PORT = doc["PORT"]
        PASS = doc["PASS"]
        NICK = doc["NICK"]

    HOST = "irc.twitch.tv"
    PORT = 6667

    NICK = "whatbotw"
    PASS = "oauth:4gpejukvczmf8yp4nqsyi3s13pe4xa"  # Throwaway account


def run_chat():
    while 1:
        readbuffer = ""
        print("#Connecting")
        s = socket.socket()
        print("#...")
        s.connect((HOST, PORT))
        print("#Connected")

        s.send(bytes("PASS %s\r\n" % PASS, "UTF-8"))
        s.send(bytes("NICK whatbotw\r\n", "UTF-8"))
        s.send(bytes("JOIN #sodapoppin\r\n", "UTF-8"))
        readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
        incoming_msg = str.split(readbuffer, "\n")
        readbuffer = incoming_msg.pop()

        for line in incoming_msg:
            line = str.rstrip(line)
            line = str.split(line)

            if line[0] == "PING":
                s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
            if line[1] == "PRIVMSG":
                sender = ""
                for char in line[0]:
                    if char == "!":
                        break
                    if char != ":":
                        sender += char
                size = len(line)
                i = 3
                message = ""
                while i < size:
                    message += line[i] + " "
                    i += 1
                print(sender + " : " + message[1:])
                # Print whole message if no connection:
                # print(message)

# MAIN #
setup()
print(HOST)
# run_chat()
