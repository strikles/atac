from .Send import Send

import json, sys, socket, time
import argparse

# import jaraco.logging
import irc.client

links = None

"""`
class IRCCat(irc.client.SimpleIRCClient):

    def __init__(self, target):
        irc.client.SimpleIRCClient.__init__(self)
        self.target = target

    def on_welcome(self, connection, event):
        if irc.client.is_channel(self.target):
            connection.join(self.target)
        else:
            self.send_it()

    def on_join(self, connection, event):
        self.send_it()

    def on_disconnect(self, connection, event):
        sys.exit(0)

    def send_it(self):
        while 1:
            line = sys.stdin.readline().strip()
            if not line:
                break
            self.connection.privmsg(self.target, line)
        self.connection.quit("Using irc.client.py")




def on_connect(connection, event):
    sys.stdout.write("\nGetting links...")
    sys.stdout.flush()
    connection.links()


def on_passwdmismatch(connection, event):
    print("Password required.")
    sys.exit(1)


def on_links(connection, event):
    global links

    links.append((event.arguments[0], event.arguments[1], event.arguments[2]))


def on_endoflinks(connection, event):
    global links

    print("\n")

    m = {}
    for (to_node, from_node, desc) in links:
        if from_node != to_node:
            m[from_node] = m.get(from_node, []) + [to_node]

    if connection.get_server_name() in m:
        if len(m[connection.get_server_name()]) == 1:
            hubs = len(m) - 1
        else:
            hubs = len(m)
    else:
        hubs = 0

    print(
        "%d servers (%d leaves and %d hubs)\n" % (len(links), len(links) - hubs, hubs)
    )

    print_tree(0, [], connection.get_server_name(), m)
    connection.quit("Using irc.client.py")


def on_disconnect(connection, event):
    sys.exit(0)


def indent_string(level, active_levels, last):
    if level == 0:
        return ""
    s = ""
    for i in range(level - 1):
        if i in active_levels:
            s = s + "| "
        else:
            s = s + "  "
    if last:
        s = s + "`-"
    else:
        s = s + "|-"
    return s


def print_tree(level, active_levels, root, map, last=0):
    sys.stdout.write(indent_string(level, active_levels, last) + root + "\n")
    if root in map:
        list = map[root]
        for r in list[:-1]:
            print_tree(level + 1, active_levels[:] + [level], r, map)
        print_tree(level + 1, active_levels[:], list[-1], map, 1)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('server')
    parser.add_argument('nickname')
    parser.add_argument('-p', '--port', default=6667, type=int)
    jaraco.logging.add_arguments(parser)
    return parser.parse_args()


def servermap(self):
    global links

    args = get_args()
    jaraco.logging.setup(args)

    links = []

    reactor = irc.client.Reactor()
    sys.stdout.write("Connecting to server...")
    sys.stdout.flush()
    try:
        c = reactor.server().connect(args.server, args.port, args.nickname)
    except irc.client.ServerConnectionError as x:
        print(x)
        sys.exit(1)

    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("passwdmismatch", on_passwdmismatch)
    c.add_global_handler("links", on_links)
    c.add_global_handler("endoflinks", on_endoflinks)
    c.add_global_handler("disconnect", on_disconnect)

    reactor.process_forever()




def main():
    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    nickname = sys.argv[2]
    target = sys.argv[3]
    c = IRCCat(target)
    try:
        c.connect(server, port, nickname)
    except irc.client.ServerConnectionError as x:
        print(x)
        sys.exit(1)
    c.start()
"""


class SendIRC(Send):

    RPL_LIST = "322"
    RPL_LISTEND = "323"
    RPL_NAMREPLY = "353"
    RPL_ENDOFNAMES = "366"

    def __init__(
        self, encrypted_config=True, config_file_path="auth.json", key_file_path=None
    ):
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

        print(
            "USER {username} {hostname} {servername} :{realname}..".format(**self.user)
        )
        self.socket.send(
            bytes(
                "USER {username} {hostname} {servername} :{realname}\r\n".format(
                    **self.user
                ).encode()
            )
        )
        #
        print("NICK {nick}...".format(**self.user))
        self.socket.send(bytes("NICK {nick}\r\n".format(**self.user).encode()))
        #
        print("PRIVMSG NICKSERV IDENTIFY {botnick} {botpass}..".format(**self.irc))
        self.socket.send(
            "PRIVMSG NICKSERV :IDENTIFY {botnick} {botpass}\r\n".format(
                **self.irc
            ).encode()
        )
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
                    self.socket.send(
                        bytes("PONG {}\r\n".format(ping_response).encode())
                    )
                    #
                    print(
                        "PRIVMSG NICKSERV IDENTIFY {botnick} {botpass}..".format(
                            **self.irc
                        )
                    )
                    self.socket.send(
                        "PRIVMSG NICKSERV :IDENTIFY {botnick} {botpass}\r\n".format(
                            **self.irc
                        ).encode()
                    )
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
