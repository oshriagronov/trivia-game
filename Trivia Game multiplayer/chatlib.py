# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occurred
	"""
    # Implement code ...
	full_msg = ""
	# Cmd check section
	if len(cmd) > CMD_FIELD_LENGTH:
		return ERROR_RETURN
	elif len(data) > MAX_DATA_LENGTH:
		return ERROR_RETURN
	if len(cmd) < CMD_FIELD_LENGTH:
		full_msg += cmd
		for i in range(16 - len(cmd)):
			full_msg +=" "
	else:
		full_msg += cmd
	full_msg += '|'

	# Data check section
	num_data = len(data)
	len_field =len(str(num_data))
	if num_data <= MAX_DATA_LENGTH:
		for i in range(LENGTH_FIELD_LENGTH - len_field):
			full_msg += '0'
		full_msg += str(num_data) + '|'
	full_msg += data
	# Return the full message
	return full_msg





def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occurred, returns None, None
	"""
	# The function should return 2 values
    # Implement code ...
	if data.count('|') < 2:
		return (ERROR_RETURN, ERROR_RETURN)	
	data = data.split('|')
	cmd = data[0].replace(' ', '')
	len_msg = data[1].replace(' ', '')
	msg = data[2]
	if len_msg.isnumeric():
		if int(len_msg) < 0 or int(len_msg) > MAX_DATA_LENGTH or int(len_msg) < int(len(msg)):
			return (ERROR_RETURN, ERROR_RETURN)

		return cmd, msg
	else:
		return (ERROR_RETURN, ERROR_RETURN)

	
def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occurred, returns None
	"""
	# Implement code ...
	check = msg.split('#')
	if len(check) == expected_fields + 1:
		return check

	else:
		return ERROR_RETURN


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	# Implement code ...
	data = '#'.join(msg_fields)
	return data

def main():
	pass

if __name__ == '__main__':
	main()