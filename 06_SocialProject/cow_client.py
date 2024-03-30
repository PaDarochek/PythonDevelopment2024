#!/usr/bin/env python3
import cmd
import threading
import time
import readline
import sys
import socket
import select

mutex = threading.Lock()
waiting_recv = False

class simple(cmd.Cmd):
    def __init__(self, socket: socket.socket, completekey: str = "tab", stdin = None, stdout = None) -> None:
        super().__init__(completekey, stdin, stdout)
        self.socket = socket

    def do_login(self, arg):
        self.socket.sendall(f'login {arg}\n'.encode())
    
    def complete_login(self, text, line, begidx, endidx):
        global waiting_recv
        global mutex
        words = (line[:endidx] + ".").split()
        options = []
        if len(words) == 2:
            mutex.acquire()
            waiting_recv = True
            self.socket.sendall('cows\n'.encode())
            options = self.socket.recv(1024).rstrip().decode().split(', ')
            waiting_recv = False
            mutex.release()
        return [c for c in options if c.startswith(text)]
    
    def do_who(self, arg):
        self.socket.sendall(f'who {arg}\n'.encode())

    def do_cows(self, arg):
        self.socket.sendall(f'cows {arg}\n'.encode())
    
    def do_yield(self, arg):
        self.socket.sendall(f'yield {arg}\n'.encode())
    
    def do_say(self, arg):
        self.socket.sendall(f'say {arg}\n'.encode())
    
    def complete_say(self, text, line, begidx, endidx):
        global waiting_recv
        global mutex
        words = (line[:endidx] + ".").split()
        options = []
        if len(words) == 2:
            mutex.acquire()
            waiting_recv = True
            self.socket.sendall('who\n'.encode())
            options = self.socket.recv(1024).rstrip().decode().split(': ')[1].split(', ')
            waiting_recv = False
            mutex.release()
        return [c for c in options if c.startswith(text)]

    def do_quit(self, arg):
        self.socket.sendall(f'quit {arg}\n'.encode())
        self.socket.close()
        exit(0)


def receive(s: socket.socket, cmdline):
    global waiting_recv
    global mutex
    while True:
        if mutex.locked():
            time.sleep(0.5)
            continue
        mutex.acquire()
        try:
            s.setblocking(False)
            msg = s.recv(1024).rstrip().decode()
            if len(msg) > 0:
                print(f"\n{msg}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)
        except OSError as err:
            if 'Bad file descriptor' in repr(err):
                mutex.release()
                break
        except:
            pass
        try:
            s.setblocking(True)
        except:
            pass
        mutex.release()


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    cmdline = simple(s)
    timer = threading.Thread(target=receive, args=(s, cmdline))
    timer.start()
    cmdline.cmdloop()
