import time
import winsound
import socket


host = '192.168.your.IP'
port = 13

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

while(1):
    song = client.recv(1024)
    song = song.decode()
    
    winsound.PlaySound(song, winsound.SND_ASYNC)
    print('Now playing: '+song)
    time.sleep(3)
