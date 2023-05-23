from flask import Flask, request


class MLOpsPipeline:

    app = Flask(__name__)

    def __init__(self, HOST='0.0.0.0', PORT=12345) -> None:
        self.HOST = HOST
        self.PORT = PORT
    
    def train(self, start_msg, end_msg, color):
        colors = {
            "HEADER": "\033[95m",
            "OKBLUE": "\033[94m",
            "OKCYAN": "\033[96m",
            "OKGREEN": "\033[92m",
            "WARNING": "\033[93m",
            "FAIL": "\033[91m",
            "ENDC": "\033[0m"
        }

        if color not in colors:
            colors_list = [key for key in colors.keys()]
            colors_list = ", ".join(colors_list)
            raise ValueError(
                "Color is not a valid color name! Valid color names are:\n{}".format(colors_list)
            )

        def decorator(func):

            @self.app.route('/train', methods=['POST'])
            def wrapper(*args, **kwargs):
                print(
                    "{}{}...{}".format(
                        colors[color],
                        start_msg,
                        colors["ENDC"]
                    )
                )

                command = request.get_data().decode()
                func(*args, **kwargs)

                print(
                    "{}{}. {}".format(
                        colors[color],
                        end_msg,
                        colors["ENDC"]
                    )
                )

                return 'Command received successfully'

            return wrapper

        return decorator
                
    def run(self):
        self.app.run(host=self.HOST, port=self.PORT)
    