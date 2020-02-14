import socket
import random
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.your.ip', 13))
server.listen(5)
conlist = []

music = [r'C:\Users\alisy\Desktop\music\sunflower.wav',r'C:\Users\alisy\Desktop\music\chanel.wav',r'C:\Users\alisy\Desktop\music\sayso.wav',r'C:\Users\alisy\Desktop\music\secrets.wav']
musicnum = 0

while True:
    connection, address = server.accept()
    conlist.append(connection)
    print('Got connection from', address)

    signal = connection.recv(1024).decode()
    if signal[0]<signal[1]<signal[2]<signal[3]<signal[4]<signal[5]<signal[6]<signal[7]<signal[8]<signal[9] and sum(signal)>1:
        connection.send(music[random.randint(0,3)]

    for c in conlist:
        strc = str(c)
        if "'192.168.speaker.ip'" in strc:
            c.send(signal.encode())
    print(signal)
