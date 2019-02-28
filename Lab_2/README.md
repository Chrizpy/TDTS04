LAB 2



chrak250 


User manual - Network Ninny



Setup


This network ninny is written in python and therefore makes it quite simple to use. Some things to consider before using this proxy is to make sure that the browser of your choice is using the port that you're running this proxy on. You will be able to choose which proxy port to use with this program.

Now when you've decided which port you want to run this proxy on and have set up your browser accordingly, you can start running this program.

Depending on the operating system you use, this can look different.

For windows user it might look like this in the command prompt:


py ninny.py


For Mac and Linux users it might look like this:


python3 ninny.py


Depending on which python installation you have, it may differ.


Running the program


To run this program, you need to specify which port you want to run the proxy on. This is done on the command line right after starting the proxy, it can look like this:


python3 ninny.py 8080


You can also make use of a debugging feature by adding an extra integer after the port number between 6-10 to set the debugging level. Which can look like this:


python3 ninny.py 8080 6