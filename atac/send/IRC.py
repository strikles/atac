from ..Send import Send

import socket
import time`
import sys`

class SendIRC(Send):
    """ A class used to represent a Configuration object

    Attributes
    ----------
    key : str
        a encryption key
    data : dict
        configuration data
    encrypted_config : bool
        use an encrypted configuration file
    config_file_path : str
        path to the configuration file
    key_file_path : str
        path to encryption key file
    gpg : gnupg.GPG
        python-gnupg gnupg.GPG

    Methods
    -------
    """

    def __init__(self, encrypted_config=True, config_file_path='auth.json', key_file_path=None):
        """ Class init

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
        self.chat = self.data['chat']
        # self.irc = socket.socket()
        # Define the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def send(self, channel, msg):
        # Transfer data
        self.irc.send(bytes("PRIVMSG " + channel + " " + msg + "\n", "UTF-8"))

    def connect(self, server, port, channel, botnick, botpass, botnickpass):
        # Connect to the server
        print("Connecting to: " + server)
        self.irc.connect((server, port))
        # Perform user authentication
        self.irc.send(bytes("USER " + botnick + " " + botnick +" " + botnick + " :python\n", "UTF-8"))
        self.irc.send(bytes("NICK " + botnick + "\n", "UTF-8"))
        self.irc.send(bytes("NICKSERV IDENTIFY " + botnickpass + " " + botpass + "\n", "UTF-8"))
        time.sleep(5)
        # join the channel
        self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))

    def get_response(self):
        time.sleep(1)
        # Get the response
        resp = self.irc.recv(2040).decode("UTF-8")
        if resp.find('PING') != -1:
            self.irc.send(bytes('PONG ' + resp.split().decode("UTF-8") [1] + '\r\n', "UTF-8"))
            return resp

    def run(self):
        ## IRC Config
        server = "10.x.x.10" # Provide a valid server IP/Hostname
        port = 6697
        channel = "#python"
        botnick = "techbeamers"
        botnickpass = "guido"
        botpass = "<%= @guido_password %>"
        #
        self.irc.connect(server, port, channel, botnick, botpass, botnickpass)
        #
        while True:
            text = self.irc.get_response()
            print(text)

            if "PRIVMSG" in text and channel in text and "hello" in text:
                self.irc.send(channel, "Hello!")


def test():
    #
    RPL_NAMREPLY   = '353'
    RPL_ENDOFNAMES = '366'
    #
    irc = {
        'host':          'chat.freenode.net',
        'port':          6667,
        'channel':       '#raspiuserguide',
        'namesinterval': 5
    }
    #
    user = {
        'nick':       'botnick',
        'username':   'botuser',
        'hostname':   'localhost',
        'servername': 'localhost',
        'realname':   'Raspberry Pi Names Bot'
    }
    #
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    print('Connecting to {host}:{port}...'.format(**irc))
    try:
        s.connect((irc['host'], irc['port']))
    except socket.error:
        print('Error connecting to IRC server {host}:{port}'.format(**irc))
        sys.exit(1)

    s.send('NICK {nick}\r\n'.format(**user).encode())
    s.send('USER {username} {hostname} {servername} :{realname}\r\n'.format(**user).encode())
    s.send('JOIN {channel}\r\n'.format(**irc).encode())
    s.send('NAMES {channel}\r\n'.format(**irc).encode())

    read_buffer = ''
    names = []

    while True:
        read_buffer += s.recv(1024).decode()
        lines = read_buffer.split('\r\n')
        read_buffer = lines.pop();
        for line in lines:
            response = line.rstrip().split(' ', 3)
            response_code = response[1]
            if response_code == RPL_NAMREPLY:
                names_list = response[3].split(':')[1]
                names += names_list.split(' ')
            if response_code == RPL_ENDOFNAMES:
                print('\r\nUsers in {channel}:'.format(**irc))
                for name in names:
                    print(name)
                names = []
                time.sleep(irc['namesinterval'])
                s.send('NAMES {channel}\r\n'.format(**irc).encode())
