import threading
import socket

host = '0.0.0.0'  # here we put the ip of the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345
server.bind((host, port))
server.listen(2)
clients = []
change=0

import re

def is_valid_message(message):
    # Define a regular expression pattern for "int,int" format
    pattern = r'^\d+,\d+$'

    # Use the re.match() function to check if the message matches the pattern
    if re.match(pattern, message):
        return True
    else:
        return False

class Board():
    def __init__(self):
        self.board = []
        for row in range(0, 3):
            a = []
            for column in range(0, 3):
                a.append(" ")
            self.board.append(a)

    def display_single_row(self, lista):
        return str(lista[0]) + " | " + str(lista[1]) + " | " + str(lista[2]) + " | "

    def get_board_str(self):
        return self.display_single_row(
            self.board[0]) + "\n" + "______________\n" + self.display_single_row(
            self.board[1]) + "\n" + "______________\n" + self.display_single_row(
            self.board[2]) + "\n"

    def add_move_x(self, lista):
        self.board[int(lista[0])][int(lista[1])] = "X"

    def add_move_o(self, lista):
        self.board[int(lista[0])][int(lista[1])] = "O"

    def verify_move(self, lista):
        if self.board[int(lista[0])][int(lista[1])] == " ":
            return True
        return False

    def verify_win(self):
        if self.board[0][0] == self.board[0][1] == self.board[0][2] and self.board[0][0] != " ":
            return str(self.board[0][0]) + " has won\n"
        elif self.board[1][0] == self.board[1][1] == self.board[1][2] and self.board[1][0] != " ":
            return str(self.board[1][0]) + " has won\n"
        elif self.board[2][0] == self.board[2][1] == self.board[2][2] and self.board[2][0] != " ":
            return str(self.board[2][0]) + " has won\n"
        elif self.board[0][0] == self.board[1][0] == self.board[2][0] and self.board[0][0] != " ":
            return str(self.board[0][0]) + " has won\n"
        elif self.board[0][1] == self.board[1][1] == self.board[2][1] and self.board[0][1] != " ":
            return str(self.board[0][1]) + " has won\n"
        elif self.board[0][2] == self.board[1][2] == self.board[2][2] and self.board[0][2] != " ":
            return str(self.board[0][2]) + " has won\n"
        elif self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return str(self.board[0][0]) + " has won\n"
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[2][0] != " ":
            return str(self.board[2][0]) + " has won\n"
        return ""


board = Board()


def broadcast():
    for i in clients:
        i.send((board.get_board_str() + "\n").encode('ascii'))
def broadcast_message(message):
    for j in clients:
        j.send(message.encode('ascii'))

def close_clients():
    for x in clients:
        x.close()

def handle(client,par):
    global change
    while True:
        try:
            if board.verify_win() != "":
                message = board.verify_win()
                broadcast_message(message)
                close_clients()
                break
            if (change %2==0 and par==0) or (change %2==1 and par==1):
                if change % 2 == 0:
                    message = "your move as X:\n"
                    client.send(message.encode('ascii'))
                else:
                    message = "your move as O:\n"
                    client.send(message.encode('ascii'))
                message = client.recv(1024)
                message_str = message.decode()
                cleaned_string = message_str.replace("\r\n", "")
                while is_valid_message(cleaned_string)==False:
                    message = "invalid input.Try again\n"
                    client.send(message.encode('ascii'))
                    message = client.recv(1024)
                    message_str = message.decode()
                    cleaned_string = message_str.replace("\r\n", "")
                lista = cleaned_string.split(",")
                if board.verify_move(lista):
                    if change%2==0:
                        board.add_move_x(lista)
                    else:
                        board.add_move_o(lista)
                    broadcast()
                    change+=1
                else:
                    message = "invalid move.Try again\n"
                    client.send(message.encode('ascii'))
            else:
                if client.recv(1024):
                    message = "not your turn\n"
                    client.send(message.encode('ascii'))
        except IOError as e:
            print(e)
            client.close()
            break


# main function to receive clients
def receive(change_1=0):
    while True:
        print("Server is running and listening ...")
        client, address = server.accept()
        print("Connected with {} ".format(str(address)))
        client.send('Connected to server!\nyour input moves should look like row,column\n'.encode('ascii'))
        clients.append(client)
        thread = threading.Thread(target=handle, args=(client,change_1))
        change_1+=1
        thread.start()


if __name__ == "__main__":
    receive()
