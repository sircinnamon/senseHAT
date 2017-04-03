#Grab a key from an external file with the format "[key_name]:[key]"
keyfile_name = "keyfile"

def get_key(key_name):
	with open(keyfile_name) as f:
		keylist = f.readlines()
	for x in keylist:
		if(x.split(":"))[0] == key_name:
			return x.split(":")[1].strip()
	print(str("Key "+key_name+" not found."))
	return None
