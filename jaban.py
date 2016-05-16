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
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,self.PORT))
                s.listen(5)

                conn_list.append(s)
                conn_list.append(sys.stdin)
                
                # Select loop for listen
                while self.running == True:
                    #inputready,outputready,exceptready = select.select ([self.conn],[self.conn],[])
                    inputready,outputready,exceptready = select.select (conn_list,[],[])

                    for sock in inputready:
                        #New connection
                        if sock == s:
                            # Handle the case in which there is a new connection recieved through server_socket
                            self.conn, self.addr = s.accept()
                            conn_list.append(self.conn)
                            print "Client (%s, %s) connected" % self.addr
                    
                    #for input_item in inputready:
                        #else:
                        # Handle sockets
                            try:

                                data = self.conn.recv(4096)
                                if data:

                                    in_data = message().break_message(data)

                                    print in_data
                                    if in_data["type"] == "\x04":

                                        print "type is correct"
                                        if in_data["flag"] == "1":
                                            print "flag is correct"
                                            print "in_data source: " + in_data["source"]
                                            print "self address: " + self.addr[0]+":"+str(self.addr[1])                                        
                                            print routing.neighbour_t_add(in_data["source"], self.addr[0]+":"+str(self.addr[1]), 5)
                                            routing.display_n_table()
                                            print "self.conn"
                                            print self.conn
                                            print conn_list
                                            if routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1] == self.conn :
                                                self.conn.sendall(Message().ack())
                                                
                                                print "added to neighbour table"
                                                routing.display_n_table()
                                            else: 
                                                print self.conn
                                                print routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1]
                                    print "\r" + "(%s, %s): " % self.addr + in_data["source"]
                            except:
                        #else:
                                break
                    time.sleep(0)

            def kill(self):
                self.running = 0
     
    class Chat_Client(threading.Thread):

            def __init__(self):
                threading.Thread.__init__(self)
                self.host = None
                self.sock = None
                self.running = 1

            def run(self):
                PORT = int(raw_input("Insert neighbour port: "))
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, PORT))
                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready = select.select ([self.sock],[self.sock],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.sock.recv(1024)
                        if data:
                            print "\r" + "(%s, %s): " % (self.host, PORT) + data
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
                        chat_server.kill()
                        self.kill()
                    elif text == 'connect_neighbour':
                        chat_client.host = raw_input("Insert neighbour ip: ")
                        chat_client.start()
                    elif text == 'auth_msg':
                        auth_str = Message().auth_successful()
                        #print auth_st
                        #auth_str get authent string
                        chat_client.sock.sendall(auth_str)

                        try:
                            chat_client.sock.sendall(text)
                            #chat_client.kill()
                        except:
                            Exception

                        try:
                            chat_server.conn.sendall(text)
                        except:
                            Exception

                    time.sleep(0)

            def kill(self):
                self.running = 0

    # Prompt, object instantiation, and threads start here.

    PORT = raw_input("Insert my port: ")
    routing = router()
    routing.myUUID = packet().source()
    routing.myIPSOC = PORT
    chat_server = Chat_Server()
    chat_server.PORT = int(PORT)
    chat_client = Chat_Client()
    chat_server.start()
    text_input = Text_Input()
    text_input.start()

if __name__ == "__main__":
    main()