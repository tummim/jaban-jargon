from Crypto.Cipher import AES
import base64
import os

class encryption(object):
	
	
		
	# the block size for the cipher object; must be 16, 24, or 32 for AES
	global BLOCK_SIZE
	BLOCK_SIZE = 32
	# the character used for padding--with a block cipher such as AES, the value
	# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
	# used to ensure that your value is always a multiple of BLOCK_SIZE
	global PADDING 
	PADDING = '{'
	# one-liner to sufficiently pad the text to be encrypted
	global pad 
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

	# one-liners to encrypt/encode and decrypt/decode a string
	# encrypt with AES, encode with base64
	
	

	# generate a random secret key
	secret = os.urandom(BLOCK_SIZE)

	# create a cipher object using the random secret
	global cipher 
	cipher = AES.new(secret)

	# encode a string
	#encoded = EncodeAES(cipher, 'password')
	#return encoded
	#print 'Encrypted string:', encoded

	# decode the encoded string
	#decoded = DecodeAES(cipher, encoded)
	#print 'Decrypted string:', decoded	

	def encrypt(self, data):
		EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
		encoded = EncodeAES(cipher, data)
		return encoded

	def decrypt(self, data):
		DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
		decoded = DecodeAES(cipher, data)
		return decoded
#sample usage
if __name__ == "__main__":
	
	en = encryption()
	print en.encrypt("Silvia")
	#print en.decrypt("g3LKYMRjSi5DmRtT4XEtOIQimN85hmBkDv3iPOWxu78=")
