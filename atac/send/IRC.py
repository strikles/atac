from .Send import Send

import json
import sys
import socket
import time


class SendIRC(Send):

    RPL_LIST = "322"
    RPL_LISTEND = "323"
    RPL_NAMREPLY = "353"
    RPL_ENDOFNAMES = "366"

    def __init__(self, encrypted_config=True, config_file_path="auth.json", key_file_path=None):
        """Class init

        Parameters
        ----------
        encrypted_config : bool
            use an encrypted configuration file
        config_file_path : str
            path to the configuration file
        key_file_path : str
            path to encryption key file
        """
        super().__init__(encrypted_config, config_file_path, key_file_path)
        self.irc = self.data["irc"]["network"]
        self.user = self.data["irc"]["user"]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        #
        print("Connecting to {host}:{port}...".format(**self.irc))
        try:
            self.socket.connect((self.irc["host"], int(self.irc["port"])))
        except socket.error:
            print("Error connecting to IRC server {host}:{port}".format(**self.irc))
            sys.exit(1)

        print("USER {username} {hostname} {servername} :{realname}..".format(**self.user))
        self.socket.send(bytes("USER {username} {hostname} {servername} :{realname}\r\n".format(**self.user).encode()))
        #
        print("NICK {nick}...".format(**self.user))
        self.socket.send(bytes("NICK {nick}\r\n".format(**self.user).encode()))
        #
        print("PRIVMSG NICKSERV IDENTIFY {botnick} {botpass}..".format(**self.irc))
        self.socket.send("PRIVMSG NICKSERV :IDENTIFY {botnick} {botpass}\r\n".format(**self.irc).encode())
        #
        print("JOIN {channel}...".format(**self.irc))
        self.socket.send(bytes("JOIN {channel}\r\n".format(**self.irc).encode()))

    """
    def get_response(self):
        time.sleep(1)
        # Get the response
        resp = self.irc.recv(2040).decode("UTF-8")
        if resp.find('PING') != -1:
            self.socket.send(bytes('PONG ' + resp.split().decode("UTF-8")[1] + '\r\n', "UTF-8"))
            return resp
    """

    def list_channels(self):
        #
        self.connect()
        #
        read_buffer = ""
        channels = []
        pinged = False
        while True:
            #
            response = self.socket.recv(2048).decode(errors="replace")
            read_buffer += response
            lines = read_buffer.split("\r\n")
            read_buffer = lines.pop()
            #
            for line in lines:
                #
                if not line:
                    continue
                #
                response = line.rstrip().split(" ", 3)
                response_code = response[1]
                print("response_code {} ...\r\n".format(response_code))
                #
                if line.find("PING") != -1:
                    ping_response = line.split()[1]
                    print("PONG {}".format(ping_response))
                    self.socket.send(bytes("PONG {}\r\n".format(ping_response).encode()))
                    #
                    print("PRIVMSG NICKSERV IDENTIFY {botnick} {botpass}..".format(**self.irc))
                    self.socket.send("PRIVMSG NICKSERV :IDENTIFY {botnick} {botpass}\r\n".format(**self.irc).encode())
                    print("LIST...")
                    self.socket.send(bytes("LIST\r\n".encode()))
                    break
                #
                if response_code == self.RPL_LIST:
                    print("GOT: {}".format(line))
                    channels_list = response[3].split(":")[1]
                    cl = channels_list.split(" ")
                    print("ch on server {}...".format(json.dumps(cl, indent=4)))
                    """
                    if cl[0] != "[+nt]" and len(cl) > 1:
                        channels += cl[1]
                    """

    def list_names(self):
        #
        self.connect()
        print("NAMES {channel}...".format(**self.irc))
        self.socket.send("NAMES {channel}\r\n".format(**self.irc).encode())
        read_buffer = ""
        names = []
        while True:
            #
            response = self.socket.recv(1024).decode()
            read_buffer += response
            lines = read_buffer.split("\r\n")
            #
            for line in lines:
                #
                if not line:
                    continue
                #
                response = line.rstrip().split(" ", 3)
                response_code = response[1]
                if response_code == self.RPL_NAMREPLY:
                    names_list = response[3].split(":")[1]
                    names += names_list.split(" ")
                #
                if response_code == self.RPL_ENDOFNAMES:
                    print("\r\nUsers in {channel}:".format(**self.irc))
                    for name in names:
                        print(name)
                    names = []
