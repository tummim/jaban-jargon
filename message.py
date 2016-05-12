

#version 1
#source 8
#destination 8
#type 1
#flag 1
#hop count 1
#length 1
#payload 79

#sum 100 Bytes


class message:
	def version():
		#Version - The protocol version. - (Integer in a single byte)
		return 1

	def source():
		#Source - Source UUID - (ASCII String)
		return 

	def destination():
		#Destination - Destination UUID - (ASCII String)

	def type():
		#Type - Distinguishes between types of message - (Integer in a single byte)

	def flag():
		#Flags - Indicate message characteristics - (Integer in a single byte)

	def hopCount(preHops):
		#Hop count -Remaining amount of hops - (Integer in a single byte)
		return int(preHops)-1

	def length():
		#Length - Length of the payload - (Integer in a single byte)

	def payload():
		#Payload - The content of the message - (ASCII String)