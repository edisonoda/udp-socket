from common import *

from socket import *

IP = '127.0.0.1'
PORT = 2000
SERVER = (IP, PORT)

# Cria o socket UDP (IPv4, Datagrama)
# AF_INET (Address Family - Internet)
# SOCK_DGRAM (Socket Datagram)
C_SOCKET = socket(AF_INET, SOCK_DGRAM)

# Dict para receber fora de ordem/com perdas
RECEIVED = {}

def receive_segment(args):
    # TODO: lógica de recebimento do segmento
    return

def handle_res(res, addr):
    print('Handling')
    action, args = parse_msg(res)
    action = action.decode()

    if action == 'END':
        return True
    elif action == 'ERROR':
        print(f'ERROR {" ".join(arg.decode() for arg in args)}')
    elif action == 'DATA': # Estrutura: DATA seq checksum bytes
        receive_segment(args)
    
    return False

def main():
    # IP = input('Insira o endereço IP: ')
    # PORT = int(input('Insira a porta do servidor: '))
    msg = 'GET /teste.png'

    C_SOCKET.sendto(msg.encode(), SERVER)
    end = False

    while not end:
        # Aguarda resposta (buffer de 2048) e decodifica
        res, addr = C_SOCKET.recvfrom(2048)
        end = handle_res(res, addr)

    # Encerra a conexão
    C_SOCKET.close()

if __name__ == "__main__":
    main()