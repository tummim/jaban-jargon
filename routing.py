#TODO
#Removing entries from tables
#Probably some other stuff I forgot atm

class router:
	#Routing here works as routing in RIP does.
	#Header will stay the same, exception made for hop count which will be decreased by 1. 
	#And OF COURSE the source will stay the same.
	#To forward the message, I will look in the routing table for the destination, get his VIA field, and search that VIA (which is an UUID) in my neighbor table. From there I will get the correct socket I will use for forwarding the packet.
    def __init__(self):
        self.myUUID = None #my own UUID for initial entry
        self.myIPSOC = None #my own IP and sock for initial entry
        self.neigh_table = [] # [entry nr][0 - UUID/1 - socket(ip:port)/2 - Passive Timer]  [self.myUUID, self.myIPSOC, 999]
        self.routing_table = [] # [entry nr][0 - Destination UUID/1 - via UUID/2 - cost(hops)] [self.myUUID, self.myUUID, 0]
		
    def find_route(self, destination): #finds route to destination
        i = 0
        while i < len(self.routing_table): #finds destination in routing table
            if self.routing_table[i][0] == destination:
                print "Found destination to " + destination + " via: " + self.routing_table[i][1] + " with cost: " + self.routing_table[i][2]
                destVia = self.routing_table[i][1] #Save Via from routing table to check from neigh table
                i = 1000 #cancel search, yeah its ugly
            else:
                destVia = "NONE"
            i = i + 1
        
        if destVia != "NONE": # If Via is found in routing table, enter here
            i = 0
            while i < len(self.neigh_table): #checks if via is in neigh table and gets data for it with the format [UUID, ipSock, Timer]
                if destVia == self.neigh_table[i][0]:
                    print "Found in neighbour table"
                    data = self.neigh_table[i]
                    return data
                    i = 1000 #cancel search
                else: # Some reason, Via not in neigh table
                    data = "ERROR: No entry in neigh table with UUID " + destVia
                    print data
                    return data
                    i = 1000
            i = i + 1

    def neighbour_t_add(self, nUUID, ipPORT, pTimer):
        #Each entry in the neighbor table has the UUID and socket information that 
        #indicates a connected node via the underlay network. This table is used 
        #to determine where to send an overlay packet through the underlay network.
        i = 0
        while i <= len(self.neigh_table): #checks if entry exists already and updates or adds new entry
            print "in func loop neigh_t_add"
            #print self.neigh_table
            #print len(self.neigh_table)
            #print len(self.neigh_table) == 1
            if len(self.neigh_table) > 0:
                if self.neigh_table[i][0] == nUUID:
                    print "nUUID exists"
                    self.neigh_table[i][2] = pTimer #update timer, entry already exists
                    if self.neigh_table[i][1] != ipPORT: #ip of nUUID is different, update entry
                        self.neigh_table[i][1] = ipPORT
                    i = 1000 #cancel search, yeah its ugly
            elif len(self.neigh_table) == 0:
                self.neigh_table.append([nUUID,ipPORT,pTimer]) #new neighbour, add new entry

                i = 1000 #cancel search, yeah its ugly
            i = i + 1		
            return self.neigh_table
    def neighbour_t_remove(self, nUUID):
    	#removes a row from neighbour table that with the nUUID 
    	for i in range(len(self.neigh_table)):
    		if len(self.neigh_table) > 0:
                if self.neigh_table[i][0] == nUUID:
                    del self.neigh_table[i][2]
                    del self.neigh_table[i][1]
                    del self.neigh_table[i][0]
                    print "Route to "+ nUUID +" removed!"

    def neighbour_t_clear(self):
    	self.neigh_table = []

    def find_uuid_in_neighbour_t(self,sUUID):
    	i=0
    	while i < len(self.neigh_table):
    		if self.neigh_table[i][0] == sUUID:
    			return i

    def display_n_table(self): #displays the neighbour table
        i = 0
        print "---------- Neighbour Table ----------"
        print " | " + "--UUID--" + " | " + "---IP + Port--- " + " | " + "--Timer--" + " | "
        while i <= len(self.neigh_table):
            print " | " + self.neigh_table[i][0] + " | " + self.neigh_table[i][1] + "|    " + str(self.neigh_table[i][2]) + "    | "
            i = i + 1
        return True

    def routing_t_add(self, destUUID, viaUUID, costHops):
        #The routing table is used to determine the next step of a message via an immediate 
        #neighbor towards the destination of the message. The routing table starts with one 
        #entry, which is the current node with cost 0, and will eventually contain all the 
        #systems in the connected network as a destination via a neighbor.
        i = 0
        while i <= len(self.routing_table): #checks if entry exists already and updates or adds new entry
            if self.routing_table[i][0] == destUUID and self.routing_table[i][1] == viaUUID:
                if costHops == self.routing_table[i][2]:
                    pass # Cost is same as before, do nothing
                    i = 1000 #cancel search, yeah its ugly
                elif costHops > self.routing_table[i][2]:
                    pass # New cost is bigger then old cost, set hop count to 16 - inf loop (from RIP)
                    self.routing_table[i][2] = 16
                    i = 1000 #cancel search, yeah its ugly
                elif costHops < self.routing_table[i][2]:
                    pass # New cost is smaller then old cost, update entry
                    self.routing_table[i][2] = costHops
                    i = 1000 #cancel search, yeah its ugly
            else:
                self.routing_table.append([destUUID,viaUUID,costHops]) #New entry
                i = 1000 #cancel search, yeah its ugly
            i = i + 1
            return self.routing_table

    def display_r_table(self): #displays the routing table
        i = 0
        print "---------- Routing Table ----------"
        print " | " + "--Dest UUID--" + " | " + "---Via UUID--- " + " | " + "--Cost--" + " | "
        while i < len(self.routing_table):
            print " | " + self.routing_table[i][0] + "      | " + self.routing_table[i][1] + "        |    " + self.routing_table[i][2] + "     | "
            i = i + 1  
            
        return True

    def clear_r_table(self):
    	self.routing_table = []

    def remove_from_r_table(self, destination):
    	#deletes routing table row by destination
    	i=0
    	while i < len(self.routing_table): #finds destination in routing table
            if self.routing_table[i][0] == destination
            	del elf.routing_table[i][2]
            	del elf.routing_table[i][1]
            	del elf.routing_table[i][0]
            i += 1
"""
#some test data and tests

route = router()

print "Adding test neighbours..."

nUUID = "ABCAIEUT"
ipPORT = "192.168.103.1:666"
pTimer = "104"
table = route.neighbour_t_add(nUUID, ipPORT, pTimer)

nUUID = "IASHFKFG"
ipPORT = "192.168.109.1:666"
pTimer = "120"
table = route.neighbour_t_add(nUUID, ipPORT, pTimer)

nUUID = "AOFGJATT"
ipPORT = "192.168.111.1:666"
pTimer = "150"
table = route.neighbour_t_add(nUUID, ipPORT, pTimer)

print "Adding test routing entries..."

destUUID = "ABCAIEUT"
viaUUID = "IASHFKFG"
costHops = "1"
table = route.routing_t_add(destUUID, viaUUID, costHops)

destUUID = "IASHFKFG"
viaUUID = "ABCAIEUT"
costHops = "1"
table = route.routing_t_add(destUUID, viaUUID, costHops)

destUUID = "AOFGJATT"
viaUUID = "ABCAIEUT"
costHops = "2"
table = route.routing_t_add(destUUID, viaUUID, costHops)

route.display_n_table()

route.display_r_table()

response = route.find_route("AAAAAAAA")
print "Finding best route to AAAAAAAA..."
print response

print "After cost update on last entry"

destUUID = "AOFGJATT"
viaUUID = "ABCAIEUT"
costHops = "0"
table = route.routing_t_add(destUUID, viaUUID, costHops)

route.display_r_table()

"""




