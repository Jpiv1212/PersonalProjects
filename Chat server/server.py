import socketserver
import threading
import socket, time

class TTCPRH(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    #list of currently connected clients
    clients = []

    #only one message for topic
    topics = {}

    # post <topic> /retain{optional} <message>
    # posts a message to a topic, if /retain is used, will retain the message to the topic
    def post(self,arg):
        if len(arg)<2: arg.append("")
        if arg[1] == "/retain":
            if len(arg)<3: arg.append("") # /retain with no message clears it
            TTCPRH.topics[arg[0]] = " ".join(arg[2:])
            del arg[1]
        for client in TTCPRH.clients:
            if client.checkpost(arg[0]): # is client subbed to this topic
                client.request.sendall(bytes(arg[0]+": "+" ".join(arg[1:]),"utf-8"))

    # sub <topic>
    # subscribes to a single topic, fails if already subbed. Gives retained messages for new sub
    def sub(self,arg):
        alreadyseen = []
        for topic in TTCPRH.topics: # figure out which retained messages have been seen
            if TTCPRH.topics[topic] and self.checkpost(topic):
                alreadyseen.append(topic)
        if self.checkpost(arg[0]): # check if already subscribed
            msg = "Failed: Already subsribed to "+arg[0]
            self.request.sendall(bytes(msg,"utf-8"))
            return
        self.subs.append(arg[0].split("/"))
        temp = self.subs
        self.subs = [self.subs[-1]]
        msg = ""
        for topic in TTCPRH.topics: # check through the retained topics and send message if 
            if topic not in alreadyseen and TTCPRH.topics[topic] and self.checkpost(topic):
                msg += "\n"+topic+": "+TTCPRH.topics[topic]
        self.request.sendall(bytes(msg.strip(),"utf-8"))
        self.subs = temp

    # unsub <topics...>
    # unsubscribes from all topics provided, tells you which it unsubbed from
    def unsub(self,arg):
        succ = []
        fail = []
        for topic in arg:
            if topic.split("/") in self.subs:
                succ.append(topic)
                self.subs.remove(topic.split("/"))
            else:
                fail.append(topic)
        out = ""
        if succ:
            out += "Successfully unsubbed from: " + ", ".join(succ)
        if fail:
            out += "Failed to unsub from: " + ", ".join(fail)
        self.request.sendall(bytes(out,"utf-8"))

    # exit
    # replies with the exit message and closes the connection
    def ex(self,arg):
        self.request.sendall(bytes("exit","utf-8")) #send exit ack
        self.request.shutdown(socket.SHUT_RDWR) #clear send buffer and close socket
        exit() #close the thread

    # list
    # lists out which topics are subscribed to
    def list(self,arg):
        self.request.sendall(bytes(("Found "+str(len(self.subs))+" subbed topics:\n"+"\n".join(["/".join(topic) for topic in self.subs])).strip(),"utf-8"))

    # main code, run when client connects
    def handle(self):
        print("Connection received from {}".format(self.client_address[0]))

        # list of functions and what they should call when received
        functions = {"post": self.post, "sub":self.sub, "unsub":self.unsub, "exit":self.ex, "list":self.list}
        
        cur_thread = threading.current_thread()
        TTCPRH.clients.append(self)
        self.subs=[] #list of things this client is subscribed to, starts empty
        try:
            while True:
            # self.request is the TCP socket connected to the client
                self.data = self.request.recv(1024).strip()
                if not self.data: break
                self.data = str(self.data,"utf-8").split()
                if self.data[0] in functions:
                    functions[self.data[0]](self.data[1:])
                else:
                    self.request.sendall(bytes("Unrecognized command: "+self.data[0],"utf-8"))
                print("{} wrote: {}:".format(self.client_address[0], self.data))
        except Exception as e:
            print(e)
        finally: # if there's some error or the client closes the socket, close and exit the connection
            self.request.close()
            TTCPRH.clients.remove(self)

    # check if topic is subscribed to, not called by the client directly
    def checkpost(self, topic):
        topic = topic.split("/")
        for sub in self.subs:
            print("checking",sub,topic)
            if len(sub) != len(topic):
                if sub[-1] == "#" and len(sub)<len(topic): pass
                else: continue
            for i,thing in enumerate(sub):
                if thing=="#":break
                elif thing=="+":continue
                elif thing!=topic[i]:
                    i = -1
                    break
            if i == -1: continue
            return True
        return False


if __name__ == "__main__":
    HOST, PORT = "localhost", int(input("PORT: "))

    # create a threaded server, which makes a new thread for each client connected
    server = socketserver.ThreadingTCPServer(("", PORT), TTCPRH)
    server.daemon_threads = True
    with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
        while True:
            time.sleep(2)
            print("{} active connections".format(threading.active_count()-2))
        server.shutdown()
