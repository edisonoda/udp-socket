from common import *

from socket import *

import random

SERVER = (S_IP, S_PORT)

# Cria o socket UDP (IPv4, Datagrama)
# AF_INET (Address Family - Internet)
# SOCK_DGRAM (Socket Datagram)
C_SOCKET = socket(AF_INET, SOCK_DGRAM)

FILENAME = 'test.txt'

TOTAL_SEGS = 0

LOSS_PROB = 0.05

# Dict para receber fora de ordem/com perdas
RECEIVED = {}

def write_file():
    name, ext = FILENAME.split('.', 1)
    save_name = f'{FILE_DIR}{name}_recebido.{ext}' if ext else f'{FILE_DIR}{name}_recebido'

    with open(save_name, 'wb') as f:
        for seq in sorted(RECEIVED.keys()):
            f.write(RECEIVED[seq])

def check_package_loss(seq):
    if random.random() < LOSS_PROB:
        print(f'Pacote {seq} perdido!')
        return True
    return False

# Estrutura: DATA seq checksum bytes
def receive_segment(args):
    seq, cs = args[:2]
    seq = int(seq.decode())
    cs = cs.decode()

    if check_package_loss(seq): return
    data = args[2]

    if cs != checksum(data):
        print(f'Erro (checksum) no segmento {seq + 1}')
        C_SOCKET.sendto(f'NACK {seq}'.encode(), SERVER)
    else:
        print(f'Recebido: {seq + 1}/{TOTAL_SEGS}')
        RECEIVED[seq] = data
        C_SOCKET.sendto(f'ACK {seq}'.encode(), SERVER)

def handle_res(res, addr):
    action, args = parse_msg(res)
    action = action.decode()

    if action == 'START':
        global TOTAL_SEGS
        TOTAL_SEGS = int(args[0].decode())
    elif action == 'END':
        print('Finalizado!')
        write_file()
        return True
    elif action == 'ERROR':
        print(f'ERROR {" ".join(arg.decode() for arg in args)}')
    elif action == 'DATA':
        receive_segment(args)
    
    return False

def main():
    global FILENAME
    global LOSS_PROB

    FILENAME = '/diagrama.jpg'

    # IP = input('Insira o endereço IP: ')
    # PORT = int(input('Insira a porta do servidor: '))
    msg = f'GET {FILENAME}'

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