from socket import *
import threading

ip = '127.0.0.1'
port = 2000

# Cria o socket UDP (IPv4, Datagrama)
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Padronização das ações:
# - GET arquivo.ext
# - DATA seq bytes
# - ACK seq
# - END

def parse_msg(msg):
    parts = msg.split()
    if not parts:
        return None, None
    
    # 0: ação, 1-N: outros argumentos
    return parts[0], parts[1:]

def start_transfer(filename, addr):
    if not filename:
        serverSocket.sendto('Nome do arquivo invalido!'.encode(), addr)
        return

    serverSocket.sendto(f'Iniciado {filename}!'.encode(), addr)
    # Buscar arquivo

# Protocolo simples para receber a requisição
def handle_req(msg, addr):
    action, args = parse_msg(msg)

    if action == 'GET':
        filename = args[0] if args else None
        start_transfer(filename, addr)
    elif action == 'ACK':
        serverSocket.sendto('ACK'.encode(), addr)
        # TODO: Criar outro handler (enviar próximo pacote ou lidar com perdas)
        pass

def main():
    # Porta: número maior que 1024
    # Fixa a porta (’’ escuta em todas as interfaces de rede)
    serverSocket.bind((ip, port))
    print(f'Servidor escutando no endereco: {ip}:{port}')

    while True:
        # Aguardar conexões/mensagens de clientes.
        # Bloqueia e aguarda pacote. Salva dados e IP/Porta de origem
        msg, addr = serverSocket.recvfrom(2048)
        handle_req(msg.decode(), addr)

        # serverSocket.sendto(res.encode(), addr)

if __name__ == "__main__":
    main()