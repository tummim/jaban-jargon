import socket
import threading
import select
import time
import sys
import string
from send_message import *
from message import *
from routing import *

#Spescial thanks to: teddy_k

def main():

    class Chat_Server(threading.Thread):
            
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
                self.conn = None
                self.addr = None
                self.PORT = None

            def socet_data (self, sock, message):
            #Do not send the message to master socket and the client who has send us the message
                for socket in conn_list:
                    if socket != s and socket == sock:
                        try :
                            socket.send(message)
                        except :
                            # broken socket connection 
                            socket.close()
                            conn_list.remove(socket)

            def run(self):
                HOST = ''
                conn_list = []
                conn_out_list = []
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,self.PORT))
                s.listen(5)

                conn_list.append(s)
                conn_list.append(sys.stdin)
                
                # Select loop for listen
                while self.running == True:
                    #inputready,outputready,exceptready = select.select ([self.conn],[self.conn],[])
                    inputready,outputready,exceptready = select.select (conn_list,conn_out_list,[])

                    for sock in inputready:
                        #New connection
                        if sock == s:
                            # Handle the case in which there is a new connection recieved through server_socket
                            self.conn, self.addr = s.accept()
                            conn_list.append(self.conn)
                            print "Client (%s, %s) connected" % self.addr
                            sys.stdout.flush()

                    #for input_item in inputready:
                        #else:
                        # Handle sockets
                        try:

                            data = self.conn.recv(4096)
                            if data:

                                in_data = message().break_message(data)
                                #print "data message: " + in_data
                                
                                print in_data
                                if in_data["type"] == "\x04":
                                    print "type is correct"
                                    if in_data["flag"] == "1":
                                        print "flag is correct"
                                        print "in_data source: " + in_data["source"]
                                        print "self address: " + str(self.addr[0])+":"+str(self.addr[1])                                        
                                        print "con out list: " + str(conn_out_list)
                                        print "con in list: " + str(conn_list)
                                        print "soc in list: " + str(conn_list[2]) # can't use getname()
                                        print routing.neighbour_t_add(in_data["source"], str(self.addr[0])+":"+str(self.addr[1]), 5)
                                        routing.display_n_table()
                                            #if routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1] == self.conn : #broken?
                                                #self.conn.sendall(Message().ack())
                                            #else: 
                                        print routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1] #broken?
                                elif in_data["type"] == "\x01":
                                    print "data message: "
                                    print in_data
                                    whole_inc_message = ""
                                    if in_data["flag"] == "4":
                                                #some cyckle to get all the in data
                                                #autorization
                                                #check if correct destination
                                        whole_inc_message = whole_inc_message + in_data["payload"]
                                        self.conn.sendall(Message().ack())
                                        #socet_data(self.conn, Message().ack())

                                    if in_data["flag"] =="1":
                                        whole_inc_message = whole_inc_message + in_data["payload"]
                                        print "(%s): %s" % in_data["source"], whole_inc_message #in_data["payload"]
                                        self.conn.sendall(Message().ack())

                                elif in_data["type"] == "\x02":
                                    if in_data["flag"] == "4":
                                        print "ack received: " + in_data["source"]

                                    #print "\r" + "(%s, %s): " % self.addr + in_data["source"]
                            
                        except Exception, e:
                        #else:
                            #print "Server e: "
                            #print e
                            break
                    
                    sys.stdout.flush()
                    time.sleep(0)

            def kill(self):
                self.running = 0
     
    class Chat_Client(threading.Thread):

            def __init__(self):
                threading.Thread.__init__(self)
                #self.host = None
                self.sock = None
                #self.port = None
                self.HOST = None
                self.PORT = None
                self.running = 1

            def run(self): 
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.sock.bind(('', self.port))
                self.sock.connect((self.HOST, int(self.PORT)))
                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready = select.select ([self.sock],[self.sock],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.sock.recv(4096)
                        if data:
                            in_data = message().break_message(data)
                            #print "data message: " + str(in_data)
                                    
                            print in_data
                            if in_data["type"] == "\x04":
                                print "type is correct"
                                if in_data["flag"] == "1":
                                    if routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1] == self.sock : #broken?
                                        self.sock.sendall(Message().ack())
                                    else: 
                                        print routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1] #broken?
                                
                            elif in_data["type"] == "\x01":
                                print "data message: "
                                print in_data
                                whole_inc_message = ""
                                if in_data["flag"] == "4":
                                                #some cyckle to get all the in data
                                                #autorization
                                                #check if correct destination
                                   whole_inc_message = whole_inc_message + in_data["payload"]
                                   self.sock.sendall(Message().ack())

                                elif in_data["flag"] =="5":
                                    whole_inc_message = whole_inc_message + in_data["payload"]
                                    print "(%s): %s" % in_data["source"], whole_inc_message #in_data["payload"]
                                    self.sock.sendall(Message().ack())
                            elif in_data["type"] == "\x02":
                                if in_data["flag"] == "4":
                                    print "ack received: " + in_data["source"]

                            print "\r" + "(%s, %s): " % (self.HOST, self.PORT) + data
                            sys.stdout.flush()
                        else:
                            break

                    time.sleep(0)

            def kill(self):
                self.running = 0
                
    class Text_Input(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1

            def run(self):
                while self.running == True:
                    
                    text = raw_input('')
                    if text == 'kill_me':
                        try:
                            chat_server.kill()
                            sys.stdout.flush()
                        except Exception, e:
                            print e
                        try:
                            chat_client.kill()
                            sys.stdout.flush()
                        except Exception, e:
                            print e    
                        try:
                            self.kill()
                            sys.stdout.flush()
                        except Exception, e:
                            print e
                    elif text == 'connect_neighbour':
                        chat_client.HOST = raw_input("Insert neighbour ip: ")
                        chat_client.PORT = int(raw_input("Insert neighbour port: "))
                        chat_client.start()
                    elif text == 'auth_msg':
                        auth_str = Message().auth_successful()
                        #print auth_str
                        #auth_str get authent string
                        chat_client.sock.sendall(auth_str)
                    else:
                    #check if message is longer than max limit and make it into an array
                        whole_message = message().payload(text)
                        print whole_message
                        try:
                            for i in range(len(whole_message)):
                                if i == len(whole_message):
                                    chat_client.sock.sendall(Message().chat_message(whole_message[i], True))
                                else:
                                    chat_client.sock.sendall(Message().chat_message(whole_message[i], False))
                            #chat_client.kill()
                        except Exception, e:
                            print "Text input e client: "
                            print e
                        
                        try:
                            for i in range(len(whole_message)):
                                if i == len(whole_message):
                                    chat_server.conn.sendall(Message().chat_message(whole_message[i], True))
                                else:
                                    chat_server.conn.sendall(Message().chat_message(whole_message[i], False))
                        except Exception, e:
                            print "Text input e server: "
                            print e

                    sys.stdout.flush()
                    time.sleep(0)

            def kill(self):
                self.running = 0

    # Prompt, object instantiation, and threads start here.
    
    PORT = raw_input("Insert my port: ")
    routing = router()
    routing.myUUID = packet().source()
    routing.myIPSOC = PORT
    chat_server = Chat_Server()
    chat_client = Chat_Client()
    text_input = Text_Input()
    chat_server.PORT = int(PORT)
    chat_server.start()
    text_input.start()

if __name__ == "__main__":
    main()