import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data

        turn = False
        left = False
        right = False

        if turn:
            if left:
                haptic.setLeftVibration(True)
            elif right:
                haptic.setRightVibration(True)

            import time
            time.sleep(1)
            haptic.setLeftVibration(False)
            haptic.setRightVibration(False)

def startServer():


    HOST="0.0.0.0"
    PORT=9999
    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

if __name__ == "__main__":

    if len(sys.argv) == 1:
        HOST = sys.argv[0]
        serverThread(HOST=HOST)
    elif len(sys.argv) == 2:
        HOST, PORT = sys.argv[0], sys.argv[1]
        serverThread(HOST=HOST,PORT=PORT)
    else:
        serverThread()
