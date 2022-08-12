import threading
import hashlib
import socket
import json
import uuid

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9999))
server.listen(5) # 5 is the maximum number of player that can be connected at the same time

clients = []
sessionIDS = []
publicSessionIDS = {}

def broadcast(msg : bytes) -> None:
    for client in clients:
        client.send(msg)

def pack(data : dict) -> bytes:
    return json.dumps(data).encode()

def unpack(data : bytes) -> dict:
    return json.loads(data.decode())

def client_handler(client):
    client.send(pack({'action': 'IDENTIFY'}))
    identified = False

    sessionID = None
    sha256Session = None

    while True:
        try:
            data : dict = unpack(client.recv(1024))
        except socket.error:
            break
        except json.JSONDecodeError:
            continue

        if data['action'] == 'IDENTIFY':
            if not identified:
                sessionID = uuid.uuid4().hex
                sha256Session = hashlib.sha256(sessionID.encode()).hexdigest()

                client.send(pack({'action': 'IDENTIFIED', 'session_id': sessionID, 'session_ids': publicSessionIDS}))
                broadcast(pack({'action': 'CONNECT', 'session_id': sha256Session, 'username': data['username'], 'skin': data['skin']}))

                publicSessionIDS[sha256Session] = {
                    'username': data['username'],
                    'skin': data['skin'],
                    'pos': [0, 0]
                }
                sessionIDS.append(sessionID)
                clients.append(client)
                identified = True
                print(f'IDENTIFY USR:{data["username"]} SESSION_ID:{sessionID} PUBLIC:{sha256Session}')
                continue
            else:
                client.send(pack({'action': 'DISCONNECT', 'msg': 'You are already identified'}))
                break

        if not identified: continue

        if data['session_id'] != sessionID:
            client.send(pack({'action': 'DISCONNECT', 'msg': 'Invalid session ID'}))
            break

        if data['action'] == 'MOVE':
            publicSessionIDS[sha256Session]['pos'] = data['pos']
            broadcast(pack({'action': 'MOVE', 'session_id': sha256Session, 'direction': data['direction']}))
            continue

        print(data)
        client.send(data)

    client.close()
    print(f'DISCONNECT SESSION_ID:{sessionID} PUBLIC:{sha256Session}')
    clients.remove(client)
    sessionIDS.remove(sessionID)
    del publicSessionIDS[sha256Session]
    broadcast(pack({'action': 'DISCONNECT', 'session_id': sha256Session}))

while True:
    client, address = server.accept()
    threading.Thread(target=client_handler, args=(client,)).start()
    print(f'{":".join(str(addr) for addr in address)} connected')