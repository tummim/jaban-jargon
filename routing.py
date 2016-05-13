

class router:
	#Routing here works as routing in RIP does.
	#Header will stay the same, exception made for hop count which will be decreased by 1. 
	#And OF COURSE the source will stay the same.
	#To forward the message, I will look in the routing table for the destination, get his VIA field, and search that VIA (which is an UUID) in my neighbor table. From there I will get the correct socket I will use for forwarding the packet.

	def neighbour_t:
		#Each entry in the neighbor table has the UUID and socket information that 
		#indicates a connected node via the underlay network. This table is used 
		#to determine where to send an overlay packet through the underlay network.

	def routing_t:
		#The routing table is used to determine the next step of a message via an immediate 
		#neighbor towards the destination of the message. The routing table starts with one 
		#entry, which is the current node with cost 0, and will eventually contain all the 
		#systems in the connected network as a destination via a neighbor.
