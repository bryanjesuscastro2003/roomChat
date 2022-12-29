import socket  
import threading
import tkinter as tk   
import tkinter.messagebox
from tkinter.ttk import Progressbar

nickname = ""  
host = ""
port = ""
client = {}

connected = False
actionState = "normal"
myMessage  = ""

window = tk.Tk()

def receive():
    while True:
        try: 
            message = client.recv(1024).decode("ascii")
            if str(message) == "NICK":
                global connected
                connected = True
                client.send(nickname.encode("ascii"))
            elif str(message).lower() == "exit":
                print("See you soon :)")
                raise ValueError("...")
            else:
                tk.Label(window, text = message).pack()
        except Exception as e:
            client.close()
            break

def connect():
    global nickname
    global host
    global port
    global client
    global connected
    nickname = text_username.get("1.0",'end-1c')
    host = text_target_server.get("1.0",'end-1c')
    port =  text_target_port.get("1.0",'end-1c')
    if(nickname and host and port):     
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, int(port)))
            receive_thread = threading.Thread(target = receive)
            receive_thread.start()
            connected = True
            tk.Label(window, text = "Connected ", font=20, fg="green").pack()
            tk.Button(window, text = "Disconnect", width = 40, command = connect, state = "active", bg = "red", fg = "white").pack()
            tkinter.messagebox.showinfo(message="Connected successfully")
        except:
            tkinter.messagebox.showerror(message = "Connection refused")
    else:
        tk.messagebox.showwarning(message = "Username - server - port are required")
    
def sendMessage():
    try:
        if connected:
            text = text_target_message.get("1.0",'end-1c')
            message = f"{nickname} : {text}" 
            client.send(message.encode("ascii"))
        else: 
             raise ValueError("")
    except:
        tkinter.messagebox.showerror(message = "No connected")
    finally:
        text_target_message.delete("1.0","end-1c")

##### GUI
window.title("MeetMetch")
window.geometry("400x700")

label_title = tk.Label(window, text = "Go for it! ", font=20)
label_title.pack()

label_username = tk.Label(window, text = "Your username : ")
label_username.pack()
text_username = tk.Text(window, height = 1)
text_username.insert("1.0", "bryn")
text_username.pack()

label_target_server = tk.Label(window, text = "Target server : ")
label_target_server.pack()
text_target_server = tk.Text(window, height = 1)
text_target_server.insert("1.0", "192.168.1.67")
text_target_server.pack()

label_target_port = tk.Label(window, text = "Target port : ")
label_target_port.pack()
text_target_port = tk.Text(window, height = 1)
text_target_port.insert("1.0", "9999")
text_target_port.pack()

btn_connect = tk.Button(window, text = "Connect", width = 50, command = connect, state = "active", bg = "black", fg = "white")
btn_connect.pack()
 
##########
label_target_message = tk.Label(window, text = "Write something : ")
text_target_message = tk.Text(window, height = 1, state = actionState)
btn_message = tk.Button(window, text = "Send", width = 50, command=sendMessage,  state = actionState, bg = "black", fg = "white")
label_target_message.pack()
text_target_message.pack()
btn_message.pack()
###########

window.mainloop()

