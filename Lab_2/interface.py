import subprocess
import os

class Interface:

    __host  = 8080

    def run(self):

        self.__get_params()

    def __init__(self):

        if os.name == "nt":
            subprocess.call("cls", shell=True)
        else:
            subprocess.call("clear")

        print("Welcome to Ninny! A simple HTTP proxy." "\n")
        print("Creator: chrak250" "\n")

    def __get_params(self):

        x = input("Choose proxy-port: ")

        params = x.split(" ")

        if len(params) > 3 or len(params) < 1:
            print("\nAmount of paramters are wrong, please try again.")
            exit(1)

        try:

            if len(params) == 1:
                self.__host  = int(params[0])
          
        except:
            print("Error: Wrong data type, try again.")
            exit(1)

    def get_port(self):
        return self.__host

