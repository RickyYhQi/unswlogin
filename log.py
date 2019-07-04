# -*- coding: utf-8 -*-

import paramiko
import warnings
import socket
import sys
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False
def interactive_shell(chan):
    if has_termios:
        posix_shell(chan)
    else:
        windows_shell(chan)
def posix_shell(chan):
    import select
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        print ('\r\n*** EOF\r\n',)
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


def windows_shell(chan):
    import threading
    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data.decode())
            sys.stdout.flush()
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        pass

warnings.filterwarnings(action='ignore',module='.*paramiko.*')
hostname = '129.94.242.53'
port = 22

####################################
username = 'input your username'
password = 'input your password'

####################################
s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

s.connect(hostname=hostname, port=port, username=username, password=password)


stdin, stdout, stderr = s.exec_command("echo -e '\u3000\u3000 \u3078\u3000\u3000\u3000\u3000\u3000\uFF0F| \n\u3000\u3000/\uFF3C7\u3000\u3000\u3000 \u2220\uFF3F/ \n\u3000 /\u3000\u2502\u3000\u3000 \uFF0F\u3000\uFF0F \n\u3000\u2502\u3000Z \uFF3F,\uFF1C\u3000\uFF0F\u3000\u3000 /`\u30FD \n\u3000\u2502\u3000\u3000\u3000\u3000\u3000\u30FD\u3000\u3000 /\u3000\u3000\u3009 \n\u3000 Y\u3000\u3000\u3000\u3000\u3000`\u3000 /\u3000\u3000/ \n\u3000\u25CF\u3000\u3000\u25CF\u3000\u3000\u3008\u3000\u3000/ \n\u3000()\u3000 \u3078\u3000\u3000\u3000\u3000|\u3000\uFF3C\u3008 \n\u3000\u3000> _\u3000 \u30A3\u3000 \u2502 \uFF0F\uFF0F \n\u3000 / \u3078\u3000\u3000 /\u3000\uFF1C| \uFF3C\uFF3C \n\u3000 \u30FD_\u3000\u3000(_\uFF0F\u3000 \u2502\uFF0F\uFF0F \n\u3000\u30007\u3000\u3000\u3000\u3000\u3000\u3000\u3000|\uFF0F \n\u3000\u3000\uFF1E\u2015r\uFFE3\uFFE3`\u2015\uFF3F\n\u6211\u662F\u4E00\u53EA\u4E1C\u5317\u5473\u513F\u7684\u76AE\u5361\u4E18 \n\u7785\u5565\u5462!!!!    \u02CB\uFE3F\u02CA\uFE40-# \n\u653E\u4E0B\u8BA2\u4E66\u5668\uFF01\uFF01\uFF01( #\uFF40\u0414\u00B4)\n\u8981\u4E0D\u7136\u7684\u8BDD\uFF0C\u6211\u5C31\u7528(o\uFF40\u0437\u2019*)\n\u6211\u7684\u4EE5\u5DF4 \u256C (\uFF40\u03B5\u00B4)\n\u7535\u4F60( *\uFF40\u03C9\u00B4)\n\nIf you want to exit\njust type exit at command line'");
print (stdout.read())

channel = s.invoke_shell()
interactive_shell(channel)


channel.close()
s.close()



