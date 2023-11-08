# Trivia Game(with local server)
![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
<br>
The project is a trivia game running by a local server(your PC) with "database"(dictionary)

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Acknowledgements](#acknowledgements)

## General info
- The server has a score system so you can compete with your friends to see who has a higher score! :smile:
- The server has a database of users, the admin(the PC who stores the files) can add and remove users from the database.
- The server has a question database, currently the database has only two questions(because it was used for testing) but you can add more!
	
## Technologies
Project is created with:
* python version: 3.9.
* socket - Library used to set up a local server and to send messages between the server with an ip address to the client and back.
* select - The library tells the kernel to notify when any of the descriptors in the sets are ready for read/write/exception conditions.
* time - library used to create a delay so the user could see the messages.
* chatlib - A custom library that has all the custom functions that make the client and server messages correct according to the protocol we created.

## Features
- The server and the client use the TCP protocol to communicate.
- You have a dictionary database of users and for every user you have a dictionary inside that dictionary, and inside there: password, score, number of questions asked.
- You have a dictionary database of questions, the admin can add more questions.
- A custom library that is responsible for building messages with correct structure according to the protocol.

## Screenshots
> server booting.

![pic1](./assets/pic2.png)


> Example of process of game.

![pic1](./assets/pic1.png)

## Setup
* First of all you need to install python on your computer and write your ip in both server and client script.
1. Download all the files.
2. Open cmd/terminal from the folder where you downloaded the project.
3. Run the following commands
```bash
python trivia_server.py
```
4. Open another terminal/cmd in from project folder and run the following command:
```
python trivia_client.py
```

### Known issues
* If you close the server and run it immediately then it will give you error that the port or the ip already catch so you need to wait a while and then it will work

## Acknowledgements
I would like to thank CampusIL and the team behind the Network.py course!
> Link to the course home page [here](https://campus.gov.il/course/cs-gov-cs-networkpy103-2020-1/)
