from common import *

from socket import *
import os

FILE_DIR = 'files'

IP = '127.0.0.1'
PORT = 2000

SEG_SIZE = 512

# Estrutura: { 'filename': [seg0, seg1, ...] }
FILES = {}

# Estrutura: {
#   'IP:PORT': {
#       'filename': name
#       TODO: outros parâmetros para controle de fluxo
#       'acked': list (ou set?),
#       'seq': 0
#       'wnd_size': n,
#   }
# }
CLIENTS = {}

# Cria o socket UDP (IPv4, Datagrama)
S_SOCKET = socket(AF_INET, SOCK_DGRAM)

def segment_file(filename):
    with open(FILE_DIR + filename, 'rb') as f:
        while True:
            seg = f.read(SEG_SIZE)
            if not seg:
                break
            yield seg

def formatted_client(addr):
    c_ip, c_port = addr
    return f'{c_ip}:{c_port}'

def start_transfer(filename, addr):
    if not filename:
        S_SOCKET.sendto('ERROR 400: Nome do arquivo invalido!'.encode(), addr)
        return

    if filename[0] != '/':
        filename = '/' + filename
    
    if not os.path.isfile(FILE_DIR + filename):
        S_SOCKET.sendto('ERROR 404: Arquivo nao encontrado!'.encode(), addr)
        return

    CLIENTS[formatted_client(addr)] = { 'filename': filename }

    # Caso o arquivo não tenha sido segmentado
    if filename not in FILES.keys():
        FILES[filename] = list(segment_file(filename))
        total = len(FILES[filename])
    
    # TODO: mover o envio de segmentos por ACK
    # Temporário
    for seq in range(total):
        send_segment(filename, seq, addr)
    S_SOCKET.sendto(b'END', addr)

    # send_segment(filename, 0, addr)
    # print(f'Transferência iniciada para: ({addr}) {filename}')

def send_segment(filename, seq, addr):
    data = FILES[filename][seq]
    cs = checksum(data)

    header = f'DATA {seq} {cs} '.encode()

    S_SOCKET.sendto(header + data, addr)

# Protocolo simples para receber a requisição
def handle_req(msg, addr):
    action, args = parse_msg(msg)

    if action == 'GET':
        filename = args[0] if args else None
        start_transfer(filename, addr)
    # TODO: ACK com controle de fluxo por cliente
    # elif action == 'ACK':
    #     seq = int(args[0]) if args else None
    #     send_segment(filename, seq, addr)
    elif action == 'NACK':
        seq = int(args[0]) if args else None
        client = CLIENTS[formatted_client(addr)]

        if client:
            send_segment(client['filename'], seq, addr)

def main():
    # Porta: número maior que 1024
    # Fixa a porta (’’ escuta em todas as interfaces de rede)
    S_SOCKET.bind((IP, PORT))
    print(f'Servidor escutando no endereco: {IP}:{PORT}')

    while True:
        # Aguardar conexões/mensagens de clientes.
        # Bloqueia e aguarda pacote. Salva dados e IP/Porta de origem
        msg, addr = S_SOCKET.recvfrom(2048)
        handle_req(msg.decode(), addr)

        # serverSocket.sendto(res.encode(), addr)

if __name__ == "__main__":
    main()