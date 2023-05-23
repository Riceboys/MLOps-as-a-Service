from flask import Flask, request
import socket


class MLOpsPipeline:

    def __init__(self, HOST='0.0.0.0', PORT=12345) -> None:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Bind the socket to a specific host and port
            server_socket.bind((HOST, PORT))

            # Listen for incoming connections
            server_socket.listen()

            print(f"Server listening on {HOST}:{PORT}")

            # Accept incoming connections
            while True:
                self.client_socket, self.client_address = server_socket.accept()

    def respond(self):
        # Send a response (optional)
        response = "Command received successfully"
        self.client_socket.sendall(response.encode())

        # Close the client connection
        self.client_socket.close()

    def train(self):
    #def train(self, start_msg, end_msg, color):
        colors = {
            "HEADER": "\033[95m",
            "OKBLUE": "\033[94m",
            "OKCYAN": "\033[96m",
            "OKGREEN": "\033[92m",
            "WARNING": "\033[93m",
            "FAIL": "\033[91m",
            "ENDC": "\033[0m"
        }

        color = "OKBLUE"

        if color not in colors:
            colors_list = [key for key in colors.keys()]
            colors_list = ", ".join(colors_list)
            raise ValueError(
                "Color is not a valid color name! Valid color names are:\n{}".format(colors_list)
            )

        def decorator(func):

            def wrapper(*args, **kwargs):

                print(
                    "{}{}...{}".format(
                        colors[color],
                        #start_msg,
                        "training started",
                        colors["ENDC"]
                    )
                )


                # Receive data from the client
                command = self.client_socket.recv(1024).decode()
                result = func(*args, **kwargs)

                print(
                    "{}{}. {}".format(
                        colors[color],
                        #end_msg,
                        "training ended",
                        colors["ENDC"]
                    )
                )

                self.respond()

                return result
                #return 'Command received successfully'

            return wrapper

        return decorator


