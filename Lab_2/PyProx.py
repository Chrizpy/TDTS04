import socket
import sys
import _thread

HOST = ""
BUFFER = 1024


bad_url  =  b'HTTP/1.1 301 Moved Permanently\r\nDate: Fri, 15 Feb 2019 05:58:12 GMT\r\nServer: Varnish\r\nLocation: https://www.ida.liu.se/~TDTS04/labs/2011/ass2/error1.html\r\nContent-Length: 0\r\nConnection: keep-alive\r\n\r\n'
bad_cont =  b'HTTP/1.1 301 Moved Permanently\r\nDate: Fri, 15 Feb 2019 05:58:12 GMT\r\nServer: Varnish\r\nLocation: https://www.ida.liu.se/~TDTS04/labs/2011/ass2/error2.html\r\nContent-Length: 0\r\nConnection: keep-alive\r\n\r\n'

baddies = ["spongebob", "britney spears", "paris hilton", "norrkoping", "examples", "choose"] 

class PyProx:

    def __init__(self, host, port):

        try:

            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Fixing potential socket hiccup
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((host, port))
            self.server.listen()

            print("Socket was successfully created, proxy server listening for connections...")

        except:

            print("There was a problem creating the socket, proxy server exited.")
            sys.exit(1)

    def start_server(self):
        
        while 1:
            # The accepted client's socket and that client's address
            conn, cli_addr = self.server.accept()
            print("New thread starting with client: ", cli_addr)
            _thread.start_new_thread(self.client_connection, (conn, cli_addr))

        self.server.close()

    def bad_word(self, url):

        for word in baddies:

            if word in url:
                return True
        
        return False


    def client_connection(self, conn, cli_addr):

        # Get the request from client, which site client wants to browse
        data_req = conn.recv(BUFFER)
        req_url  = data_req.decode().split(" ")[1]
        req_url  = req_url.split("/")[2] 
        first    = data_req.decode().split("\n")[0]
        save     = b""
        

        if "www." in req_url:
            req_url  = req_url.split("www.")[1]


        # We only handle GET requests
        if "GET" in first:
            if self.bad_word(first):
                conn.send(bad_url)
                _thread.exit()

            try:

                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((req_url, 80))
                client_socket.send(data_req)

                dis_a_baddie = False
                check        = False

                garbage = client_socket.recv(BUFFER)
                header  = garbage.split(b'\r\n\r\n')[0]
                
                decoded_h = header.decode("utf-8")

                while 1:

                    save    += garbage

                    if "text/html" in decoded_h:
                        check = True

                    if len(garbage) > 0:
                        
                        if check:
                            print(garbage.split(b'\n')[0])
    
                            check = False
                        
                    else:
                        break      

                    garbage = client_socket.recv(BUFFER)    
                        
                if dis_a_baddie:
                    conn.send(bad_cont)
                    conn.close()
                    _thread.exit()
                

                conn.send(save)
                client_socket.close()

            except Exception as e:
                print("Something went wrong. ", e)

            finally:
                conn.close()
                print("Connection closed, thread exitted.")
                _thread.exit()

        


if __name__ == "__main__":

    proxen = PyProx(HOST, 8080)

    try:
        proxen.start_server()

    except KeyboardInterrupt:
        print("Control-C was pressed, exiting server...")
        sys.exit(1)


            
