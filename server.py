import socket
import threading
  
HOST="127.0.0.1"
PORT=1234 #port can be bw 0-65535
LISTNER_LIMIT=5
activeUser=[]

def listen_message(client,username):
    while 1:
        response=client.recv(2048).decode('utf-8')
        if response !='':
            final=username + '~' + response
            send_message(final)

        else:
            print("emptyt message {username}")
#single client
def sendtoclient(client,message):
    client.sendall(message.encode())

#funtion to send message to all clients that are connected to the server
def send_message(message):
    for user in activeUser:
        sendtoclient(user[1],message)




def client_handle(client):
    while 1:
        username=client.recv(2048).decode('utf-8')
        if username != '':
            activeUser.append((username,client))
            break


        else:
            print("username is invalid")

    threading.Thread(target=listen_message,args=(client,username)).start()


def main():
    #AF_INET means Ipv4
    #STREAM means TCP protocol
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    try:
        server.bind((HOST,PORT))
        print("running")
    except:
        print("unable to bind to host {HOST}and port{PORT}")

    server.listen(LISTNER_LIMIT)


    while 1:
        client,address=server.accept()
        print(f"server success {address[0]}{address[1]}")
        
        threading.Thread(target=client_handle, args=(client,)).start()


if __name__=="__main__":
    main()