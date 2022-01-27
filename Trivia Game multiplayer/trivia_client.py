import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****
import os
import time
SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# Build/Send/Receive message from the server functions
def build_send_recv_parse(conn, msg_code, data):
	build_and_send_message(conn, msg_code, data)
	msg_code, data = recv_message_and_parse(conn)
	return msg_code, data

def build_and_send_message(conn, code, data):
	"""
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
	full_msg = chatlib.build_message(code, data)
	conn.send(full_msg.encode())

def recv_message_and_parse(conn):
	"""
	Receives a new message from given socket,
	then parses the message using chatlib.
	Paramaters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message. 
	If error occurred, will return None, None
	"""
	full_msg = conn.recv(1024).decode()
	cmd, data = chatlib.parse_message(full_msg)
	return cmd, data

# Get information from the server functions
def play_question(conn):
	cmd, data = build_send_recv_parse(conn, "GET_QUESTION", '')
	if cmd == "ERROR":
		print("\nsomething went wrong")
		return
	
	elif cmd == "OUT_OF_QUESTION":
		print("The server run out of questions")
		return
	
	else:
		data = chatlib.split_data(data, 6)
		print(data)
		print('Q: ' + data[2] + ':\n1. ' + data[3] + '\n2. ' + data[4] + '\n3. ' + data[5]+ '\n4. ' + data[6])
		user_input = str(input("Please choose an answer: "))
		if user_input == data[1]:
			print("You answered correct!")
			build_and_send_message(conn, "SEND_ANSWER", data[0] + '#' + user_input)
		else:
			print("Wrong, the correct answer is below:\n"+ data[1])
			


def get_logged_users(conn):
	cmd, data = build_send_recv_parse(conn, "LOGGED", "")
	if cmd == 'ERROR':
		print("\nsomething went wrong..")
	else:
		print(data)


def get_score(conn):
	cmd, data = build_send_recv_parse(conn, "MY_SCORE", "")
	print("\nMy Score: " + data)

		
def get_highscore(conn):
	cmd, data = build_send_recv_parse(conn, "HIGHSCORE", "")
	if cmd == 'ERROR':
		print("\nsomething went wrong..")
	else:
		print('\nThe Score Leaderboard:\n' + data)
		return

# Connect/Login/Logout and error functions
def connect():
	func_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	func_socket.connect((SERVER_IP, SERVER_PORT))
	return (func_socket)


def error_and_exit(error_msg):
	print(error_msg)
	os.ew_exit(os.EX_OK)


def login(conn):
	cmd = ""
	while cmd != "LOGIN_OK":
		username = input("Please enter username: ")
		password = input("Please enter password: ")
		build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],username + "#" + password)
		cmd, data = recv_message_and_parse(conn)
		print(data)
	print("Logged in!")
	return

def logout(conn):
	build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"],"")
	print("Goodbye")

# Main function where all happend
def main():
    # Implement code
	my_socket = connect()
	login(my_socket)
	# Main menu of the card game
	while True:
		print("\nmain menu:\np     Play trivia question\ns     Get my score\nh     Get high score\nl     Get logged users\nq     Quit")
		user_input = input("\nyour choose: ")
		if user_input == 'p':
			play_question(my_socket)
			time.sleep(3)

		elif user_input == 's':
			get_score(my_socket)
			time.sleep(3)

		elif user_input == 'h':
			get_highscore(my_socket)
			time.sleep(3)
		
		elif user_input == 'l':
			get_logged_users(my_socket)
			time.sleep(3)
		
		elif user_input == 'q':
			logout(my_socket)
			my_socket.close()
			break

		else:
			print("this command doesn't exist!\nPlease choose one of the above.")
			time.sleep(3)
			
		os.system('clear')


	

if __name__ == '__main__':
    main()
