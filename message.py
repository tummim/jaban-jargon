

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
		return ABCDEFGH

	def destination():
		#Destination - Destination UUID - (ASCII String)

	def type():
		#Type - Distinguishes between types of message - (Integer in a single byte)
		return F

	def flag():
		#Flags - Indicate message characteristics - (Integer in a single byte)
		return 1

	def hopCount(preHops, first):
		#Hop count -Remaining amount of hops - (Integer in a single byte)
		if first== False
			return int(preHops)-1
		else
			return 15

	def length(payload_len):
		#Length - Length of the payload - (Integer in a single byte)
		return payload_len

	def payload(data):
		#Payload - The content of the message - (ASCII String)
		data=data.encode("utf8")
		total_len = len(data)
		max_len = 79
		data_array = []
		if total_len > max_len:
			for index in range(0,len(data_l),max_len):
				data_array.append(data[index:index+max_len])
		else
			data_array.append(data)

		return data_array