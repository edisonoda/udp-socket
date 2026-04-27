from common import *

from socket import *

IP = '127.0.0.1'
PORT = 2000
SERVER = (IP, PORT)

# Cria o socket UDP (IPv4, Datagrama)
# AF_INET (Address Family - Internet)
# SOCK_DGRAM (Socket Datagram)
C_SOCKET = socket(AF_INET, SOCK_DGRAM)

TOTAL_SEGS = 0

# Dict para receber fora de ordem/com perdas
RECEIVED = {}

# Estrutura: DATA seq checksum bytes
def receive_segment(args):
    seq, cs = args[:2]
    seq = int(seq.decode())
    cs = cs.decode()

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
        return True
    elif action == 'ERROR':
        print(f'ERROR {" ".join(arg.decode() for arg in args)}')
    elif action == 'DATA':
        receive_segment(args)
    
    return False

def main():
    # IP = input('Insira o endereço IP: ')
    # PORT = int(input('Insira a porta do servidor: '))
    msg = 'GET /diagrama.jpg'

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