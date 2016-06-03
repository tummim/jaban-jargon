import os, sys
import packet
from packet import *

class Message():
	
	""" DATA MESSAGES"""

	def session_message(self):
		auth_msg =  bytearray()
		build_packet =  packet()
		# Packet Fields Starts Here!!!

		auth_msg.append(build_packet.version())
		for c in build_packet.source():
			auth_msg.append(c);
		for c in build_packet.destination("00000000"):
			auth_msg.append(c);
		auth_msg.append(build_packet.type("data"))		
		
		for c in build_packet.data_flag(False, True, False, False, False, False):
			auth_msg.append(c);
		
		auth_msg.append(build_packet.hopcount(1))
		auth_msg.append(build_packet.length())
		auth_msg.append(build_packet.payload())

		return auth_msg;

	
	def file_message(self, data, last):

		file_msg = bytearray()
		build_packet =  packet()

		file_msg.append(build_packet.version())
		for c in build_packet.source():
			file_msg.append(c);
		for c in build_packet.destination("00000000"):
			file_msg.append(c);
		file_msg.append(build_packet.type("data"))		
		
		if last == True:
			for c in build_packet.data_flag(False, False, False, False, False, True):
				file_msg.append(c);
		else:
			for c in build_packet.data_flag(False, False, True, False, False, False):	
				file_msg.append(c);	
		#for c in build_packet.data_flag(False, False, True, False, False, False):
			
		
		file_msg.append(build_packet.hopcount(15))
		file_msg.append(build_packet.length(len(data)))
		file_msg.append(build_packet.payload(data))

		return file_msg;

	def chat_message(self, data, last):

		chat_msg = bytearray()
		build_packet =  packet()
		
		chat_msg.append(build_packet.version())
		for c in build_packet.source():
			chat_msg.append(c);
		for c in build_packet.destination("00000000"):
			chat_msg.append(c);
		chat_msg.append(build_packet.type("data"))		
		
		if last == True:
			for c in build_packet.data_flag(False, False, False, False, False, True):
				chat_msg.append(c);
		else:
			for c in build_packet.data_flag(False, False, False, True, False, False):
				chat_msg.append(c);
		
		chat_msg.append(build_packet.hopcount(15))
		chat_msg.append(build_packet.length(len(data)))
		for n in data:
			chat_msg.append(build_packet.payload(n.encode("utf-8")))

		return chat_msg;

	""" AUTHETICATION MESSAGES """
	def auth_successful(self): #InitiateAuth

		auth_msg = bytearray()
		build_packet =  packet()
		
		auth_msg.append(build_packet.version())
		for c in build_packet.source():
			auth_msg.append(c)
		for c in build_packet.destination("00000000"):
			auth_msg.append(c)
		auth_msg.append(build_packet.type("authentication"))		
		
		for c in build_packet.authentication_flag(False, True):
			auth_msg.append(c)
		
		auth_msg.append(build_packet.hopcount(1))
		auth_msg.append(build_packet.length(0))
		auth_msg.append(build_packet.payload(" "))

		return str(auth_msg);

	def auth_failure(self):

		auth_msg = bytearray()
		build_packet =  packet()
		
		auth_msg.append(build_packet.version())
		for c in build_packet.source():
			auth_msg.append(c);
		for c in build_packet.destination("00000000"):
			auth_msg.append(c);
		auth_msg.append(build_packet.type("authentication"))		
		
		for c in build_packet.authentication_flag(True, False):
			auth_msg.append(c);
		
		auth_msg.append(build_packet.hopcount(1))
		auth_msg.append(build_packet.length(0))
		auth_msg.append(build_packet.payload(" "))

		return auth_msg;

	""" CONTROL MESSAGES MESSAGES """

	def session_init(self):

		control_msg = bytearray()
		build_packet =  packet()
		
		control_msg.append(build_packet.version())
		for c in build_packet.source():
			control_msg.append(c);
		for c in build_packet.destination():
			control_msg.append(c);
		control_msg.append(build_packet.type("control"))		
		
		for c in build_packet.control_flag(True, False, False, False, False, False, False):
			control_msg.append(c);
		
		control_msg.append(build_packet.hopcount())
		control_msg.append(build_packet.length())
		control_msg.append(build_packet.payload())

		return control_msg;

	def file_transfer_init(self, data):

		control_msg = bytearray()
		build_packet =  packet()
		
		control_msg.append(build_packet.version())
		for c in build_packet.source():
			control_msg.append(c);
		for c in build_packet.destination():
			control_msg.append(c);
		control_msg.append(build_packet.type("control"))		
		
		for c in build_packet.control_flag(False, True, False, False, False, False, False):
			control_msg.append(c);
		
		control_msg.append(build_packet.hopcount())
		control_msg.append(build_packet.length(len(data)))
		for n in data:
			control_msg.append(build_packet.payload(n.encode("utf-8")))
		#get size of the file
		file_size=os.path.getsize('data')

		while len(control_msg) + len(file_size) != 100:
			control_msg.append('0')

		control_msg.append(file_size)
		return control_msg;

	def routing_update_init(self, data):

		control_msg = bytearray()
		build_packet =  packet()
		
		control_msg.append(build_packet.version())
		for c in build_packet.source():
			control_msg.append(c);
		for c in build_packet.destination():
			control_msg.append(c);
		control_msg.append(build_packet.type("control"))		
		
		for c in build_packet.control_flag(False, False, True, False, False, False, False):
			control_msg.append(c);
		
		control_msg.append(build_packet.hopcount(15))
		control_msg.append(build_packet.length(len(data)))
		control_msg.append(build_packet.payload(data))

		return control_msg;

	def keep_alive(self):

		control_msg = bytearray()
		build_packet =  packet()
		
		control_msg.append(build_packet.version())
		for c in build_packet.source():
			control_msg.append(c);
		for c in build_packet.destination():
			control_msg.append(c);
		control_msg.append(build_packet.type("control"))		
		
		for c in build_packet.control_flag(False, False, False, True, False, False, False):
			control_msg.append(c);
		
		control_msg.append(build_packet.hopcount())
		control_msg.append(build_packet.length())
		control_msg.append(build_packet.payload())

		return control_msg;

	def ack(self):

		control_msg = bytearray()
		build_packet =  packet()
		
		control_msg.append(build_packet.version())
		for c in build_packet.source():
			control_msg.append(c);
		for c in build_packet.destination():
			control_msg.append(c);
		control_msg.append(build_packet.type("control"))		
		
		for c in build_packet.control_flag(False, False, False, False, True, False, False):
			control_msg.append(c);
		
		control_msg.append(build_packet.hopcount(15))
		control_msg.append(build_packet.length(0))
		control_msg.append(build_packet.payload(" "))

		return control_msg;

	def seq_num(self):

		control_msg = bytearray()
		build_packet =  packet()
		
		control_msg.append(build_packet.version())
		for c in build_packet.source():
			control_msg.append(c);
		for c in build_packet.destination():
			control_msg.append(c);
		control_msg.append(build_packet.type("control"))		
		
		for c in build_packet.control_flag(False, False, False, False, False, True, False):
			control_msg.append(c);
		
		control_msg.append(build_packet.hopcount())
		control_msg.append(build_packet.length())
		control_msg.append(build_packet.payload())

		return control_msg;

	def rst(self):

		control_msg = bytearray()
		build_packet =  packet()
		
		control_msg.append(build_packet.version())
		for c in build_packet.source():
			control_msg.append(c);
		for c in build_packet.destination():
			control_msg.append(c);
		control_msg.append(build_packet.type("control"))		
		
		for c in build_packet.control_flag(False, False, False, False, False, False, True):
			control_msg.append(c);
		
		control_msg.append(build_packet.hopcount())
		control_msg.append(build_packet.length())
		control_msg.append(build_packet.payload())

		return control_msg;





if __name__ == "__main__":
	
	mg = Message()
	print mg.auth_successful()
	#print mg.file_message()
	#print mg.chat_message()
	#print mg.auth_successful()
	#print mg.auth_failure()