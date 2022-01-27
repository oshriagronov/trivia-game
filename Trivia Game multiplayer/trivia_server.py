##############################################################################
# server.py
##############################################################################
import select
import socket
from typing import final
import chatlib

#### GLOBALS - i have global generator(declare with main function) he is for the question to save memory usage
users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later
answer_global = ""
client_sockets = []

ERROR_MSG = "Error! "
'''
don't change the ip or the port, 127.0.0.1 is a special address, aka INADDR_LOOPBACK, that means "bind localhost only on the loopback device". 
There's no way to reach anything but the local host itself on that socket.
'''
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


##### HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
	global message_to_send
	## copy from client
	ip = socket.socket.getpeername(conn)
	full_msg = chatlib.build_message(code, msg)
	print("[SERVER] " + str(ip) + " msg: " + full_msg)	  # Debug print
	conn.send(full_msg.encode())	


def recv_message_and_parse(conn):
	## copy from client
	full_msg = conn.recv(1024).decode()
	ip = socket.socket.getpeername(conn)
	print("[CLIENT] " + str(ip) + " msg: " + full_msg)	 
	cmd, data = chatlib.parse_message(full_msg)
	return cmd, data
	


###### Data Loaders 

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Receives: -
	Returns: questions dictionary
	"""
	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Receives: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]},
			"oshri"		:	{"password":"password","score":0,"questions_asked":[]}
			}
	return users

	
#### SOCKET

## SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Receives: -
	Returns: the socket object
	"""
	# Implement code ...
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen()
	return server_socket
	
## Socket error
	
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Receives: socket, message error string from called function
	Returns: None
	"""
	# Implement code ...
	conn.send(error_msg.encode())
	return None

## Sockets print

def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


	
##### MESSAGE HANDLING

## Question handling

def create_random_question():
	global answer_global
	questions = load_questions()
	question = ""
	for q in questions.keys():
		question += str(q) + '#' + str(questions[q]["correct"]) + "#"
		question += str(questions[q]["question"])
		for a in questions[q]["answers"]:
			question += "#" + str(a)
		yield question
		question = ""
	yield 0


def handle_question_message(conn):
	global question_gen
	random_question = next(question_gen)
	if random_question != int(0):
		build_and_send_message(conn, "YOUR_QUESTION", random_question)
	else:
		build_and_send_message(conn, "OUT_OF_QUESTION","")
		question_gen = create_random_question()
		
## Answer handling

def handle_answer_message (conn, data, username):
	load_user_database()
	questions = load_questions()
	data = data.split('#')
	if str(questions[int(data[0])]["correct"]) == str(data[1]):
		users[username]["score"] += 5



## Score handling
def handle_highscore_message(conn):
	global users
	username_list = list(users.keys())
	x = {}
	highscore_msg = ""
	for user_name in username_list:
		score = int(users[user_name]["score"])
		x[user_name] = score
	user_dict_sort = {k: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)}
	for user in user_dict_sort:
		highscore_msg += str(user) + " - " + str(user_dict_sort[user]) + '\n'
	build_and_send_message(conn, "ALL_SCORE", highscore_msg)

def handle_getscore_message(conn, username):
	global users
	# Implement this in later chapters
	score = users[username]["score"]
	build_and_send_message(conn, "YOUR_SCORE", str(score))

## Logout handling
	
def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Receives: socket
	Returns: None
	"""
	global logged_users
	global client_sockets
	# Implement code ...
	ip = socket.socket.getpeername(conn)
	logged_users.pop(ip[1])
	client_sockets.remove(conn)
	print("[SERVER]  client logout")
	conn.close()
	print_client_sockets(conn)
					

## Logged handling

def handle_logged_message(conn):
	global logged_users
	build_and_send_message(conn, "LOGGED", "Logged users:\n"+ str(logged_users))

## Login handling

def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Receives: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	users = load_user_database()
	# Implement code ...
	data = data.split('#')
	if data[0] in users.keys():
		if data[1] == users[data[0]]["password"]:
			build_and_send_message(conn, "LOGIN_OK", "")
			ip = socket.socket.getpeername(conn)
			logged_users[ip[1]] = data[0]
		else:
			build_and_send_message(conn, "ERROR", "")
		
	else:
		build_and_send_message(conn, "ERROR", "")


## Client message handling
def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Receives: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	# Implement code ...

	if cmd == "LOGIN":
		handle_login_message(conn, data)
	
	elif cmd == "MY_SCORE":
		ip = socket.socket.getpeername(conn)
		username = str(logged_users[ip[1]])
		handle_getscore_message(conn, username)

	elif cmd == "HIGHSCORE":
		handle_highscore_message(conn)
	
	elif cmd == "LOGGED":
		handle_logged_message(conn)

	elif cmd == "LOGOUT":
		handle_logout_message(conn)
		print("[SERVER]  waiting for new client")

	elif cmd == "GET_QUESTION":
		handle_question_message(conn)

	elif cmd == "SEND_ANSWER":
		ip = socket.socket.getpeername(conn)
		username = str(logged_users[ip[1]])
		handle_answer_message(conn, data, username)

	else:
		build_and_send_message(conn, "ERROR", "")
	
#### MAIN loop
def main():
	# Initializes global users and questions dictionaries using load functions, will be used later
	global users
	global questions
	global client_sockets
	global logged_users
	# Implement code ...
	message_to_send = []
	server_socket = setup_socket()
	print("Welcome to Trivia Server!\nStarting up on port " + str(SERVER_PORT) + "\nwaiting for connection...")
	while True:
		ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
		for current_socket in ready_to_read:
			if current_socket is server_socket:
				(client_socket, client_address) = current_socket.accept()
				print("New client joined! " + str(client_address))
				client_sockets.append(client_socket)
				print_client_sockets(client_sockets)
			else:
				print("New data from client")
				msg = current_socket.recv(1024).decode()
				pre_cmd, pre_data = chatlib.parse_message(msg)
				if pre_cmd == None:
					print("[SERVER] " + str(client_address) + " connection with the client lost.\nwaitting for connection...")
					if len(logged_users) > 0:
						logged_users.pop(client_address[1])
					client_sockets.remove(current_socket)
					current_socket.close()
				else:
					message_to_send.append((current_socket, msg))
		for message in message_to_send:
			current_socket, full_mess = message
			if current_socket in ready_to_write:
				cmd, data = chatlib.parse_message(full_mess)
				handle_client_message(current_socket, cmd, data)
				message_to_send.remove(message)
			else:
				print("The client:" + client_address + "is busy right now.")

if __name__ == '__main__':
	question_gen = create_random_question()
	main()
