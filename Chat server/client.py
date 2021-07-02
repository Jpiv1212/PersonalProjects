#!/usr/bin/env python
import socket, threading
import sys, time
from msvcrt import getch, getche

HOST, PORT = "localhost", 9999
HOST, PORT = input("HOST: "),int(input("PORT: "))
data = " ".join(sys.argv[1:])

line = ""
exited = threading.Event()

# special function to let output go above the prompt
def fancy_input():
    global line
    c = getch()
    while ord(c) not in (13, 3): # 13 - Enter, 3 - Ctrl+C
        if exited.is_set():
            exit()
        if ord(c) in (127, 8): # 127,8 - Backspace (Unix, Windows)
            if line:
                print("\b \b",end="",flush=True)
                line = line[:-1]
##            print("\r> "+line,end="", flush=True)
        elif ord(c) == 224: #arrow key
            getch()
        elif ord(c) in range(128):
            # decode to string if byte
            c = c.decode('ascii') if str(c)[0] == 'b' else c
            line += c
            print(c,end="", flush=True)
        c = getch()
    if ord(c) == 3: # Ctrl+C
        exit()
    print("\n> ",end="")
    beef = line
    line = ""
    return beef

# listens constantly from the server and prints anything it finds
def recv_data(sock):
    while True:
        try:
            data = str(sock.recv(1024), "utf-8")
            if exited.is_set():
                global line
                line = data
                break
            if not data: break
            print(("\r{}"+" "*len(line)+"\n> {}").format(data,line), end="")
        except KeyboardInterrupt:
            exited.set()
            break
        except ConnectionAbortedError:
            exited.set()
            break
        except Exception as e:
            print("\nHost disconnected, press any key to exit",end="",flush=True)
            exited.set()
            break

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    print("Connecting...")
    try:
        sock.connect((HOST, PORT))
    except:
        print("Could not connect to",HOST,end="")
        exit()
    print("Connected to",HOST,"on port",PORT)

    # asynchronous thread to print received data, even if
    # user hasn't pressed enter
    input_thread = threading.Thread(target=recv_data, args=(sock,))
    input_thread.daemon = True
    input_thread.start()
    
    # Connect to server and send data
    print("> ",end="", flush=True)
    while True:
        data = fancy_input()

        # if user entered 'exit', break normal flow and wait for server
        if data == "exit":
            sock.send(bytes("exit", "utf-8"))
            sock.settimeout(5) # wait for response for 5 seconds
            exited.set()
            input_thread.join()
            # wait for server response
            if line == "exit":
                print("\rClear to exit",end="")
                exit() # will kill input thread too
            else:
                print("\rExit failed, try again\n> ",end="",flush=True)
                sock.settimeout(0)
                exited.clear()
                line = ""

                #restart socket loop again
                input_thread = threading.Thread(target=recv_data, args=(sock,))
                input_thread.daemon = True
                input_thread.start()
        
        if exited.is_set():
            exit()
        try:
            if data:
                sock.send(bytes(data, "utf-8"))
        except:
            break

    # only happens if server refused sent data
    print("\rServer Disconnected: Exiting",end="")
    time.sleep(1)
