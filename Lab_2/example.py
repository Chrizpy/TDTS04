import socket 

import sys 

import _thread 

import re 

 

badwordlist=["spongebob","britney spears","paris hilton","norrkoping",] 

 

def handle_request(requeststring,connection): 

    print("Requst string as below:") 

    print(requeststring) 

    temp=requeststring.lower() 

    for word in badwordlist: 

            if ( word in temp ): 

                print("Find bad word in URL: " + word) 

                #url = "HTTP/1.1 302 Found\r\nLocation:https://www.ida.liu.se/~TDTS04/labs/2011/ass2/error1.html\r\n\r\n" 

                #connection.send(url.encode()) 

                warning="The URL has bad words.  " 

                connection.send(link.encode()) 

                print("Done with redirection (Bad URL)") 

                 

     

    hostlist = list(filter(lambda x: x.startswith('Host:'), (requeststring).split('\r\n')))[0] 

    hostlist=hostlist.split(':')[1:] 

    #print("hostlist") 

    #print(hostlist) #[' ocsp.digicert.com'] 

    #print(len(hostlist)) #1 

    webhost="" 

    webport=80 

    if (len(hostlist)==2): 

        webhost=hostlist[tdts040] 

        webport=hostlist[1] 

    if(len(hostlist)==1): 

        webhost=hostlist[0] 

        webpost=80 

    print("Information of Host and Port as below : ") 

    print("Webhost is " + webhost+"  and webport is "+ str(webport)) 

     

       

    requeststring=re.sub('gzip,deflate',"",requeststring,flags=re.IGNORECASE) 

    requeststring=re.sub('proxy-connection',"Connection",requeststring,flags=re.IGNORECASE) 

    requeststring=re.sub('keep-alive',"close",requeststring,flags=re.IGNORECASE) 

    print("Request string after modified: ") 

    print(requeststring) 

    print("End of request string") 

    return webhost,webport,requeststring   

 

 

 

 

def handle_response(webserver_s): 

    #handle response: 

    buf=b"" 

    header=True 

    not_gzip=True 

    while True: 

        response = webserver_s.recv(1024) 

        if(len(response)>0): 

            if (header): 

                header = False 

                header_info=response.split(b'\r\n\r\n')[0] 

                print("header_infor in byte: ") 

                print(header_info) 

                header_string=header_info.decode('utf-8') 

                print ("header in string: ") 

                print(header_string) 

                 

                #find out content type 

                text=True 

                c_type=True 

         

                if ("Content-Type:" in header_string): 

                    for item in header_string.split("\n"): 

                        if "Content-Type: " in item: 

                            print (item) 

                            index=item.find(";") 

                            content_type=item[14:index] 

                            print("content_type is: ") 

                            print(content_type) # text/html 

                            if "text" in content_type: 

                                text=True 

                            else: 

                                text=False 

                else: 

                    print("No content type") 

                    content_type="unknown" 

                    c_type=False 

                    text=False 

                     

                if ("Content-Encoding:" in header_string): 

                    encoding_type=list(filter(lambda x:x.startswith('Content-Encoding:'),(header_string).split('\r\n')))[0].split(':')[1:][0].strip() 

                else: 

                    print("Can not find Encoding type. ")   

                    encoding_type="unknown" 

 

                     

                #get buf (byte type) 

                buf+=response 

                #break if len(response)<1024 

                if(len(response)<1024 and ("gzip" in encoding_type)): 

                    print("Last response, gzip data, break! ") 

                    not_gzip=False 

                    break 

 

 

        else: 

            print("Length of response is 0,break!") 

            break 

                 

    if(text): 

        print("Text response! ") 

        print("Content check...") 

        print("encoding type") 

        print(encoding_type) 

        print("stuff that doesnt work") 

        print(buf) 

        buf_string=buf.decode('utf-8') 

        print("buf_string") 

        print(buf_string) 

        temp=buf_string.lower() 

        for word in badwordlist: 

            if ( word in temp ): 

                print("Find bad word in content: " + word) 

                url = "HTTP/1.1 302 Found\r\nLocation:https://www.ida.liu.se/~TDTS04/labs/2011/ass2/error2.html\r\n\r\n" 

                connection.send(url.encode()) 

                print("Done with redirection (Bad content)") 

 

                

    return buf 

 

def handle_thread(connection, address): 

    request=connection.recv(1024) #request from browser, byte form, need to be decode 

    try: 

        requeststring=request.decode('utf-8') #reqeust string form 

        

    except: 

        print("Request from browser decode failed") 

        connection.close() 

        return 

 

    if(len(requeststring)<1): 

        print("Length of Get request is 0.") 

        connection.close() 

         

    if 'GET' in requeststring: 

        #handle_request: 

        webhost,webport,request_s=handle_request(requeststring,connection) # get host,port,request string back 

        webhost=webhost.strip() 

        print("webhost is : ......................") 

        print(webhost) 

        print("webport is:..........................") 

        print(webport) 

 

         

        #start a web server socket to talk to the web server 

        webserver_s=socket.socket() 

        webserver_s.connect((webhost, webport)) 

        #send request string to webserver 

        webserver_s.send(request_s.encode()) 

        #handel response 

        buf=handle_response(webserver_s) 

        #send response to browser 

        connection.send(buf) 

        print("Socket close") 

        connection.close() 

        webserver_s.close() 

        print("Both socket closed successfully") 

     

 

if __name__ == '__main__': 

     port = 8080; 

     serversocket = socket.socket() 

     serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 

     serversocket.bind(("127.0.0.1",port))  #bind to any host 

     serversocket.listen(5) 

     print("Serversocket start to listen. ") 

     while True: 

         connection, address = serversocket.accept() 

         print("address: ") 

         print(address) 

         print("connection: ") 

         print(connection) 

         print("Start new thread") 

         _thread.start_new_thread(handle_thread,(connection, address)) 

         print("Thread end\n") 