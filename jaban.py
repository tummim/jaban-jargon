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
                self.accept_file = "no"
                self.file_name = ''

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
                

                whole_inc_message = []
                whole_file_inc_message =[]
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
                        #try:
                        try:
                            data = self.conn.recv(4096)
                        except Exception, e:
                            data = None
                            sys.stdout.flush()
                        
                        if data != None:

                            in_data = message().break_message(data)
                                #print "data message: " + in_data
                                
                            #print in_data
                            if in_data["type"] == "\x04":
                                
                                if in_data["flag"] == "1":
                                    
                                    #print "in_data source: " + in_data["source"]
                                    #print "self address: " + str(self.addr[0])+":"+str(self.addr[1])                                        
                                    #print "con out list: " + str(conn_out_list)
                                    #print "con in list: " + str(conn_list)
                                    #print "soc in list: " + str(conn_list[2]) # can't use getname()
                                    routing.neighbour_t_add(in_data["source"], str(self.addr[0])+":"+str(self.addr[1]), 5)
                                    routing.display_n_table()
                                        #if routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1] == self.conn : #broken?
                                            #self.conn.sendall(Message().ack())
                                        #else: 
                                    #print routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1] #broken?
                            elif in_data["type"] == "\x01":
                                
                                if in_data["flag"] == "4":
                                            #some cyckle to get all the in data
                                            #autorization
                                            #check if correct destination
                                    whole_inc_message.append(in_data["payload"])
                                    self.conn.sendall(Message().ack())

                                elif in_data["flag"] =="1" and self.accept_file != "y":
                                    whole_inc_message.append(in_data["payload"])
                                    print "(" + in_data["source"] + "): " + ''.join(whole_inc_message) #in_data["payload"]
                                    self.conn.sendall(Message().ack())
                                    whole_inc_message=[]

                                elif in_data["flag"] == "8" and self.accept_file == "y":
                                    print "file transfer"
                                    f = open(self.file_name, 'a')
                                    try:
                                        f.write(in_data["payload"])
                                        f.close()
                                        self.conn.sendall(Message().ack())
                                    except Exception, e:
                                        f.close()

                                elif in_data["flag"] =="1" and self.accept_file == "y":
                                    print "file transfer"
                                    f = open(self.file_name, 'a')
                                    try:
                                        f.write(in_data["payload"])
                                        f.close()
                                        self.conn.sendall(Message().ack())
                                    except Exception, e:
                                        f.close()

                                    self.accept_file = "no"    
                                    self.conn.sendall(Message().ack())
                                    sys.stdout.flush()


                            elif in_data["type"] == "\x02":
                                if in_data["flag"] == "20":
                                    file_name_l = []
                                    file_size_l = []
                                    flie_name_s = False
                                    file_size_s = False
                                    for m in in_data["payload"]:
                                        if m != "0" and flie_name_s == False:
                                            file_name_l.append(m)
                                        elif m == "0" and flie_name_s == False:
                                            flie_name_s = True
                                        elif m != "0" and flie_name_s == True:
                                            file_size_l.append(m)
                                            file_size_s = True
                                        elif m == "0" and file_size_s == True:
                                            file_size_l.append(m)
                                    
                                    self.file_name = ''.join(file_name_l)
                                    file_size = ''.join(file_size_l)

                                    print "receiving file " + self.file_name + " size: " + file_size
                                    self.accept_file = raw_input('Accept file (y/n):')
                                    self.conn.sendall(Message().ack())

                                if in_data["flag"] == "4":
                                    print "ack received: " + in_data["source"]

                                    #print "\r" + "(%s, %s): " % self.addr + in_data["source"]
                            
                        #except Exception, e:
                        else:
                            #print "Server e: "
                            #print e
                            #break
                            sys.stdout.flush()
                    
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
                self.accept_file = "no"
                self.file_name = ''
                
            def run(self): 
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.sock.bind(('', self.port))
                self.sock.connect((self.HOST, int(self.PORT)))
                
                whole_inc_message = []
                whole_file_inc_message =[]

                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready = select.select ([self.sock],[self.sock],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.sock.recv(4096)
                        if data:
                            in_data = message().break_message(data)
                            #print "data message: " + str(in_data)
                                    
                            if in_data["type"] == "\x04":
                                if in_data["flag"] == "1":
                                    if routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1] == str(self.sock) : #broken?
                                        self.sock.sendall(Message().ack())
                                    else: 
                                        print routing.neigh_table[routing.find_uuid_in_neighbour_t(in_data["source"])][1] #broken?
                                
                            elif in_data["type"] == "\x01":
                                if in_data["flag"] == "4":
                                                #some cyckle to get all the in data
                                                #autorization
                                                #check if correct destination
                                    whole_inc_message.append(in_data["payload"])
                                    self.sock.sendall(Message().ack())

                                elif in_data["flag"] == "8" and self.accept_file == "y":
                                    print "file transfer"
                                    f = open(self.file_name, 'a')
                                    try:
                                        f.write(in_data["payload"])
                                        f.close()
                                    except Exception, e:
                                        f.close()

                                    self.sock.sendall(Message().ack())
                                    sys.stdout.flush()

                                elif in_data["flag"] =="1" and self.accept_file == "y":
                                    print "file transfer"
                                    f = open(self.file_name, 'a')
                                    try:
                                        f.write(in_data["payload"])
                                        f.close()
                                        self.sock.sendall(Message().ack())
                                    except Exception, e:
                                        f.close()
                                    
                                    self.accept_file = "no"
                                    sys.stdout.flush()

                                elif in_data["flag"] =="1" and self.accept_file != "y":
                                    whole_inc_message.append(in_data["payload"])
                                    print "("+in_data["source"]+"): "+ ''.join(whole_inc_message) #in_data["payload"]
                                    whole_inc_message = []
                                    self.sock.sendall(Message().ack())

                            #file transfer init
                            elif in_data["type"] == "\x02":
                                if in_data["flag"] == "20":
                                    file_name_l = []
                                    file_size_l = []
                                    flie_name_s = False
                                    file_size_s = False
                                    for m in in_data["payload"]:
                                        if m != "0" and flie_name_s == False:
                                            file_name_l.append(m)
                                        elif m == "0" and flie_name_s == False:
                                            flie_name_s = True
                                        elif m != "0" and flie_name_s == True:
                                            file_size_l.append(m)
                                            file_size_s = True
                                        elif m == "0" and file_size_s == True:
                                            file_size_l.append(m)
                                    
                                    self.file_name = ''.join(file_name_l)
                                    file_size = ''.join(file_size_l)

                                    print "receiving file " + self.file_name + " size: " + file_size
                                    self.accept_file = raw_input('Accept file (y/n):')

                            elif in_data["type"] == "\x02":
                                if in_data["flag"] == "4":
                                    print "ack received: " + in_data["source"]



                            #print "\r" + "(%s, %s): " % (self.HOST, self.PORT) + data
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
                    elif text == 'start_serv':
                        chat_server.start()    
                    elif text == 'connect_neighbour':
                        chat_client.HOST = raw_input("Insert neighbour ip: ")
                        chat_client.PORT = int(raw_input("Insert neighbour port: "))
                        chat_client.start()
                    elif text == 'auth_msg':
                        auth_str = Message().auth_successful()
                        try:
                            chat_client.sock.sendall(auth_str)
                        except Exception, e:
                            sys.stdout.flush()
                        try:
                            chat_server.sock.sendall(auth_str)
                        except Exception, e:
                            sys.stdout.flush()
                    elif text == 'send_file':
                        file_to_send = raw_input("Type the name of the file to send: ")
                        with open(file_to_send,'rb') as fts:
                            content = fts.read()

                        whole_message = message().payload(content)
                        if len(whole_message) > 0 and whole_message != ['']:
                            try:
                                for i in range(len(whole_message)):
                                    if i == (len(whole_message)-1):
                                        chat_client.sock.sendall(Message().file_message(whole_message[i], True))
                                    else:
                                        chat_client.sock.sendall(Message().file_message(whole_message[i], False))
                            except Exception, e:
                                #print "Text input e client: "
                                #print e
                                sys.stdout.flush()

                            try:
                                for i in range(len(whole_message)):
                                    if i == (len(whole_message)-1):
                                        chat_server.conn.sendall(Message().file_message(whole_message[i], True))
                                    else:
                                        chat_server.conn.sendall(Message().file_message(whole_message[i], False))
                            except Exception, e:
                                #print "Text input e server: "
                                #print e
                                sys.stdout.flush()
                    elif text == 'routing_u':
                        routing_u_m = ''.join(routing.routing_table)
                        try:
                            chat_client.sock.sendall(Message().routing_update_init(routing_u_m))
                        except Exception, e:
                            sys.stdout.flush()
                        try:
                            chat_server.conn.sendall(Message().routing_update_init(routing_u_m))
                        except Exception, e:
                            sys.stdout.flush()
                    elif text == 'add_route':
                        destUUID = raw_input("Insert UUID of the destination: ")
                        viaUUID = raw_input("Innsert UIID of the next hop: ")
                        costHops = raw_input("Insert cost of hops: ")
                        router.routing_t_add(destUUID, viaUUID, costHops)
                        print "route added"
                    elif text == 'del_route':
                        dest = raw_input("insert a destination to be deleted: ")
                        router.remove_from_r_table(dest)
                    elif text == 'clear_rt':
                        router.clear_r_table()
                    elif text == 'show_rt':
                        routing.display_r_table()
                    elif text == 'insert_neighbour':                    
                        nUUID = raw_input("Insert UUID of the new route: ")
                        nIP = raw_input("Innsert ip of the new route: ")
                        nPORT = raw_input("Insert port of the new route: ")
                        routing.neighbour_t_add(nUUID,nIP+":"+nPORT, 30)
                        print "neighbour added"
                    elif text == 'del_neighbour':
                        dUUID = raw_input("Insert UUID to be romoved from routing table: ")
                        if len(dUUID) != 0:
                            routing.neighbour_t_remove(self, dUUID)
                    elif text == 'clear_nt':
                        routing.neighbour_t_clear()
                        print "Neighbour table cleared"
                    elif text == 'ack':
                        try:
                            chat_server.conn.sendall(Message().ack())
                        except Exception, e:
                            sys.stdout.flush()
                        try:
                            chat_client.sock.sendall(Message().ack())
                        except Exception, e:
                            sys.stdout.flush()
                    else:
                    #check if message is longer than max limit and make it into an array
                        whole_message = message().payload(text)
                        if len(whole_message) > 0 and whole_message != ['']:
                            try:
                                for i in range(len(whole_message)):
                                    if i == (len(whole_message)-1):
                                        chat_client.sock.sendall(Message().chat_message(whole_message[i], True))
                                    else:
                                        chat_client.sock.sendall(Message().chat_message(whole_message[i], False))
                            except Exception, e:
                                #print "Text input e client: "
                                #print e
                                sys.stdout.flush()

                            try:
                                for i in range(len(whole_message)):
                                    if i == (len(whole_message)-1):
                                        chat_server.conn.sendall(Message().chat_message(whole_message[i], True))
                                    else:
                                        chat_server.conn.sendall(Message().chat_message(whole_message[i], False))
                            except Exception, e:
                                #print "Text input e server: "
                                #print e
                                sys.stdout.flush()

                    sys.stdout.flush()
                    time.sleep(0)

            def kill(self):
                self.running = 0

    # Prompt, object instantiation, and threads start here.
    
    PORT = raw_input("Insert my port: ")
    routing = router()
    routing.myUUID = raw_input("insert my UUID (8 characters): ").encode("ASCII")
    pakk = packet()
    pakk.uuid = routing.myUUID
    routing.myIPSOC = "127.0.0.1:"+PORT
    #add 1. data to routing and neighbour table
    routing.neighbour_t_add(routing.myUUID,routing.myIPSOC, 30)
    routing.routing_t_add(routing.myUUID, routing.myUUID, 0)
    chat_server = Chat_Server()
    chat_client = Chat_Client()
    text_input = Text_Input()
    chat_server.PORT = int(PORT)
    text_input.start()

if __name__ == "__main__":
    main()