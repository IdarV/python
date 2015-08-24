#! /usr/bin/env python


import socket


def find_between(sting, first, last):
    try:
        start = sting.index(first) + len(first)
        end = sting.index(last, start)
        return sting[start:end]
    except ValueError:
        return ""


HOST = "irc.twitch.tv"
PORT = 6667

NICK = "whatbotw"
PASS = "oauth:4gpejukvczmf8yp4nqsyi3s13pe4xa"  # Throwaway account
IDENT = "whatbotw"
REALNAME = "whatbotw"
MASTER = "ido"

readbuffer = ""
print("#Connecting")
s = socket.socket()
print("#...")
s.connect((HOST, PORT))
print("#Connected")

s.send(bytes("PASS %s\r\n" % PASS, "UTF-8"))
s.send(bytes("NICK whatbotw\r\n", "UTF-8"))
s.send(bytes("JOIN #sodapoppin\r\n", "UTF-8"))

while 1:
    readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
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
            print(find_between(line[0], ":", "!") + " : " + message[1:])