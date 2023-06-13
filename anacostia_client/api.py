from flask import Flask, request

global running


class AnacostiaPipeline:

    app = Flask(__name__)

    colors = {
        "HEADER": "\033[95m",
        "OKBLUE": "\033[94m",
        "OKCYAN": "\033[96m",
        "OKGREEN": "\033[92m",
        "WARNING": "\033[93m",
        "FAIL": "\033[91m",
        "ENDC": "\033[0m"
    }


    def __init__(self, HOST: str = '0.0.0.0', PORT: int = 12345) -> None:
        self.HOST = HOST
        self.PORT = PORT
    
    def train(self, start_msg, end_msg, color):
        if color not in self.colors:
            colors_list = [key for key in self.colors.keys()]
            colors_list = ", ".join(colors_list)
            raise ValueError(
                "Color is not a valid color name! Valid color names are:\n{}".format(colors_list)
            )

        def decorator(func):

            @self.app.route('/train', methods=['POST'])
            def train_wrapper(*args, **kwargs):
                print(
                    "{}{}...{}".format(
                        self.colors[color],
                        start_msg,
                        self.colors["ENDC"]
                    )
                )

                command = request.get_data().decode()
                func(*args, **kwargs)

                print(
                    "{}{}. {}".format(
                        self.colors[color],
                        end_msg,
                        self.colors["ENDC"]
                    )
                )

                return 'Train command received successfully'

            return train_wrapper

        return decorator
                
    def prepare_data(self, start_msg, end_msg, color):
        if color not in self.colors:
            colors_list = [key for key in self.colors.keys()]
            colors_list = ", ".join(colors_list)
            raise ValueError(
                "Color is not a valid color name! Valid color names are:\n{}".format(colors_list)
            )

        def decorator(func):

            @self.app.route('/prepare-data', methods=['POST'])
            def prepare_data_wrapper(*args, **kwargs):
                print(
                    "{}{}...{}".format(
                        self.colors[color],
                        start_msg,
                        self.colors["ENDC"]
                    )
                )

                command = request.get_data().decode()
                func(*args, **kwargs)

                print(
                    "{}{}. {}".format(
                        self.colors[color],
                        end_msg,
                        self.colors["ENDC"]
                    )
                )

                return 'Prepare data command received successfully'

            return prepare_data_wrapper

        return decorator
    
    def run(self):
        self.app.run(host=self.HOST, port=self.PORT)
    