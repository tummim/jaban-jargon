import sys, os#, json, gnupg
import ConfigParser

config =  ConfigParser.ConfigParser()
config.add_section('Global');
config.set('Global', 'source', '796326ED')

#class pgp: 

	#def key(self):
	#	gpg = gnupg.GPG(gnupghome="/home/bolaji/.gnupg")
	#	import_result = gpg.recv_keys('keyserver.ubuntu.com', '796326ED')
	#	fingerprint = import_result.fingerprints
	#	return "796326ED";

class packet():
	"""This is the Message Class"""

	config =  ConfigParser.ConfigParser()

	def version(self , ver = 0x01):		
		return ver;


	def source(self, uuid=""):
		#pgps = pgp()
		#uuid = pgps.key()
		config.read('config.ini')
		uuid = config.get('Global', 'source')
		return uuid.encode("ASCII");
		


	def destination(self, dst = " "):
		return dst;

	def type(self, messsage_type):
		if (messsage_type == "data"):
			typ = 0x01;
		if (messsage_type == "control"):
			typ = 0x02;
		if (messsage_type == "authentication"):
			typ = 0x04
		return typ;
	#print type
	#def flags(self, routing_update, authentication_data, chat_messsage, txt_msg_data, seq_num, fragment_num):
	def data_flag(self, routing_update, session, file_data, message_data, seq_num, fragment):
		
		dataflag = 0x00 
		routing = 0
		auth = 0
		message = 0
		seq = 0
		frag = 0
		
		if (routing_update == True):
			routing = 0x20
		if (session == True):
			auth = 0x10
		if (message_data == True):
			message = 0x04
		if (seq_num == True):
			seq = 0x02
		if (fragment == True):
			frag = 0x01

		dataflag = routing + auth + message + seq + frag	
		#print dataflag
		return str(dataflag)

	def control_flag(self, session_init, file_transfer, routing_update_init, keep_alive, ack, seq_num, rst):
		
		controlflag = 0 
		session = 0
		filetransfer = 0
		routing = 0
		keepalive = 0
		ackn = 0
		seq = 0
		reset = 0
		if (session_init == True):
			session = 0x40
		if (file_transfer == True):
			filetransfer = 0x20
		if (routing_update_init == True):
			routing = 0x10
		if (keep_alive == True):
			keepalive = 0x08
		if (ack == True):
			ackn = 0x04
		if (seq_num == True):
			seq = 0x02
		if (rst == True):
			reset = 0x01

		controlflag = session + filetransfer + routing + keepalive + ackn + seq + reset

		
		return str(controlflag)

	def authentication_flag(self, auth_success, no_auth):
		
		success = 0 	
		failed = 0
		
		if (auth_success == True):
			success = 0x02
		if (no_auth == True):
			failed = 0x01
		

		authflag = success + failed
		return str(authflag)	


	def hopcount(self, hop = " "):
		return hop;

	def length(self, pay = " "):
		leng = str(len(pay));
		return leng.encode("ASCII");

	def payload(self, pay = " "):
		return pay;
"""
	def packet(self):
		#some_type = "authentication" 
		msg = packet();

		build_packet = bytearray()
		build_packet.append(msg.version())
		for c in msg.source():
			build_packet.append(c)
		#build_packet.append(msg.source())
		build_packet.append(msg.destination())
		build_packet.append(msg.type("data"))
		for c in msg.data_flag(True, False, False, True, False, False):
			build_packet.append(c)

		#build_packet.append(msg.data_flag(True, False, True, False, False, False))
		
		if (some_type == "data"):
			for c in msg.data_flag(False, True, False, False, False, True):
				build_packet.append(c)
		elif(some_type == "control"):	
			for c in msg.control_flag(False, True, False, False, False, True, False):
				build_packet.append(c)	
		elif(some_type == "authentication"): 
			for c in msg.authentication_flag(False, True):
				build_packet.append(c)		
		
		#print msg.data_flag(True, True, True, False, False, False)
		#for e in msg.flags():
			#build_packet.append(e)
		#build_packet.append(msg.flags(1))
		#build_packet.append(msg.hopcount())
		#build_packet.append(msg.length())
		#build_packet.append(msg.payload())

		return build_packet;
"""
if __name__ == "__main__":
	
	mg = packet()
	print mg.packet()
	#print mg.key()
	

	#def __init__(self, arg):
	#	super(ClassName, self).__init__()
	#	self.arg = arg
