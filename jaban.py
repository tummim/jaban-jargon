import socket
import threading
import select
import time
import sys
import string
from send_message import *
from message import *

#Spescial thanks to: teddy_k

def main():

    class Chat_Server(threading.Thread):
            
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
                self.conn = None
                self.addr = None

            def run(self):
                HOST = ''
                PORT = int(raw_input("Insert my port: "))
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,PORT))
                s.listen(1)
                self.conn, self.addr = s.accept()
                print "Client (%s, %s) connected" % self.addr
                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready = select.select ([self.conn],[self.conn],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.conn.recv(1024)
                        if data:
                            in_data = message.break_message(data)
                            print in_data
                            print "\r" + "(%s, %s): " % self.addr + in_data["source"]
                        else:
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
                            #text_input.run()
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
                    if text == 'kill_me' :
                        chat_client.kill()
                        chat_server.kill()
                        self.kill()
                    elif text == 'connect_neighbour':
                        chat_client.host = raw_input('Insert neighbour ip: ')
                        chat_client.start()
                    elif text == 'auth_msg':
                        auth_str = Message().auth_successful()
                        #print auth_str
                        #auth_str get authent string
                        chat_client.sock.sendall(auth_str)

                        
                    else:
                        try:
                            chat_client.sock.sendall(text)
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

    chat_server = Chat_Server()
    chat_client = Chat_Client()
    chat_server.start()
    text_input = Text_Input()
    text_input.start()

if __name__ == "__main__":
    main()