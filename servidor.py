from socket import *
import threading

ip = '127.0.0.1'
port = 2000

# Cria o socket UDP (IPv4, Datagrama)
serverSocket = socket(AF_INET, SOCK_DGRAM)

def main():
    # Porta: número maior que 1024
    # Fixa a porta (’’ escuta em todas as interfaces de rede)
    serverSocket.bind((ip, port))
    print(f'Servidor escutando no endereco: {ip}:{port}')

    while True:
        # Aguardar conexões/mensagens de clientes.
        # Bloqueia e aguarda pacote. Salva dados e IP/Porta de origem
        msg, addr = serverSocket.recvfrom(2048)
        data = msg.decode()

if __name__ == "__main__":
    main()