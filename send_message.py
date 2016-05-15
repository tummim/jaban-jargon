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
		for c in build_packet.destination("000000"):
			auth_msg.append(c);
		auth_msg.append(build_packet.type("data"))		
		
		for c in build_packet.data_flag(False, True, False, False, False, False):
			auth_msg.append(c);
		
		auth_msg.append(build_packet.hopcount(1))
		auth_msg.append(build_packet.length())
		auth_msg.append(build_packet.payload())

		return auth_msg;

	
	def file_message(self):

		file_msg = bytearray()
		build_packet =  packet()

		file_msg.append(build_packet.version())
		for c in build_packet.source():
			file_msg.append(c);
		for c in build_packet.destination("000000"):
			file_msg.append(c);
		file_msg.append(build_packet.type("data"))		
		
		for c in build_packet.data_flag(False, False, True, False, False, False):
			file_msg.append(c);
		
		file_msg.append(build_packet.hopcount(1))
		file_msg.append(build_packet.length())
		file_msg.append(build_packet.payload())

		return file_msg;

	def chat_message(self):

		chat_msg = bytearray()
		build_packet =  packet()
		
		chat_msg.append(build_packet.version())
		for c in build_packet.source():
			chat_msg.append(c);
		for c in build_packet.destination("000000"):
			chat_msg.append(c);
		chat_msg.append(build_packet.type("data"))		
		
		for c in build_packet.data_flag(False, False, False, True, False, False):
			chat_msg.append(c);
		
		chat_msg.append(build_packet.hopcount(1))
		chat_msg.append(build_packet.length())
		chat_msg.append(build_packet.payload())

		return chat_msg;

	""" AUTHETICATION MESSAGES """
	def auth_successful(self):

		auth_msg = bytearray()
		build_packet =  packet()
		
		auth_msg.append(build_packet.version())
		for c in build_packet.source():
			auth_msg.append(c);
		for c in build_packet.destination("000000"):
			auth_msg.append(c);
		auth_msg.append(build_packet.type("authentication"))		
		
		for c in build_packet.authentication_flag(True, False):
			auth_msg.append(c);
		
		auth_msg.append(build_packet.hopcount(1))
		auth_msg.append(build_packet.length())
		auth_msg.append(build_packet.payload())

		return str(auth_msg);

	def auth_failure(self):

		auth_msg = bytearray()
		build_packet =  packet()
		
		auth_msg.append(build_packet.version())
		for c in build_packet.source():
			auth_msg.append(c);
		for c in build_packet.destination("000000"):
			auth_msg.append(c);
		auth_msg.append(build_packet.type("authentication"))		
		
		for c in build_packet.authentication_flag(False, True):
			auth_msg.append(c);
		
		auth_msg.append(build_packet.hopcount(1))
		auth_msg.append(build_packet.length())
		auth_msg.append(build_packet.payload())

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

	def file_transfer_init(self):

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
		control_msg.append(build_packet.length())
		control_msg.append(build_packet.payload())

		return control_msg;

	def routing_update_init(self):

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
		
		control_msg.append(build_packet.hopcount())
		control_msg.append(build_packet.length())
		control_msg.append(build_packet.payload())

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
		
		control_msg.append(build_packet.hopcount())
		control_msg.append(build_packet.length())
		control_msg.append(build_packet.payload())

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
	print mg.rst()
	#print mg.file_message()
	#print mg.chat_message()
	#print mg.auth_successful()
	#print mg.auth_failure()