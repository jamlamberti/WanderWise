import socket
import sys
import os
from threading import Thread, Event
import select
import Queue
class SocketClient(object):
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__connect(host, port)
    def __connect(self,host, port):
        self.s.connect((host, port))
    def send(self, msg):
        self.s.sendall(msg)
    def recv(self):
        msg = self.s.recv(2048)
        self.__close()
        return msg
    def __close(self):
        self.s.close()

class SocketServer(object):
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
    def listen(self):
        self.s.listen(5)
        self.conn, addr = self.s.accept()
        return self.conn.recv(2048)
    def send(self, msg):
        self.conn.sendall(msg)
        self.conn.close()
def print_wrapper(s):
    print s
    return s
class AsyncSocketServer(object):
    def __init__(self, host, port, callback=print_wrapper):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.stop_event = Event()
        self.callback = callback
        self.worker_thread = None
    def __start(self):
        pass
    def start(self):
        self.stop_event.clear()
        if self.worker_thread is None:
            self.worker_thread = Thread(target=self.run)
            self.worker_thread.start()
            print "It's running"
    def stop(self):
        if self.worker_thread is not None:
            self.stop_event.set()
            #self.worker_thread.join()
    def listen(self):
        self.s.listen(5)
    def run(self):
        inputs = [self.s]
        outputs = []
        message_queues = {}
        while inputs:
            #print "Here"
            if self.stop_event.is_set():
                print "Got stop event"
                break
            #print "selecting"
            readable, writable, exceptional = select.select(inputs, outputs, inputs, 0)
            #print "done"
            for s in readable:
                #print "0"
                if s is self.s:
                    conn, addr = s.accept()
                    conn.setblocking(0)
                    inputs.append(conn)
                    message_queues[conn] = Queue.Queue()
                else:
                    data = s.recv(2048)
                    if data:
                        print "Received %s from %s"%(data, s.getpeername())
                        # Use the callback
                        # TODO: This code can be simplified since our packets aren't segmented
                        resp = self.callback(data)
                        message_queues[s].put((data, resp))
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del message_queues[s]
            for s in writable:
                #print "1"
                try:
                    _, next_msg = message_queues[s].get_nowait()
                except Queue.Empty:
                    outputs.remove(s)
                else:
                    s.send(next_msg)
                    outputs.remove(s)
            for s in exceptional:
                #print "2"
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del message_queues[s]
    def accept(self):
        conn, addr = self.s.accept()
        return conn, addr
    def send(self, conn, msg):
        self.conn.sendall(msg)
        self.conn.close()

def testServer():
    ss = SocketServer('', 12345)
    msg = ss.listen()
    assert msg == "Hello World"
    ss.send(msg)
def testClient():
    sc = SocketClient('127.0.0.1', 12345)
    sc.send("Hello World")
    assert sc.recv() == "Hello World"
    #sc.__close()

def testAsync():
    import time
    asc = AsyncSocketServer('', 12345, callback=print_wrapper)
    asc.listen()
    asc.start()
    time.sleep(1)
    asc.stop()

def test():
    from threading import Thread
    import time
    server = Thread(target=testServer())
    server.start()
    print "Server running"
    client = Thread(target=testClient())
    client.start()
    print "Client running"
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        # fork and execv
        if os.fork() == 0:
            testClient()
        else:
            testServer()
            print "Passed Socket Tests"
            if os.fork() == 0:
               testClient()
            else:
                testAsync()
                print "Passed Async tests"

