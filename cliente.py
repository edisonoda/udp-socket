from socket import *

# ip = input('Insira o endereço IP: ')
# port = int(input('Insira a porta do servidor: '))
IP = '127.0.0.1'
PORT = 2000

# Cria o socket UDP (IPv4, Datagrama)
# AF_INET (Address Family - Internet)
# SOCK_DGRAM (Socket Datagram)
C_SOCKET = socket(AF_INET, SOCK_DGRAM)

def main():
    msg = 'GET /teste.png'
    C_SOCKET.sendto(msg.encode(), (IP, PORT))

    recebidos = []

    # simulação perda

    # recepção
    # verificar integridade segmentos
    # Aguarda resposta (buffer de 2048) e decodifica
    resp, addr = C_SOCKET.recvfrom(2048)
    print('Servidor:', resp.decode())
    recebidos.append(resp.decode())

    # montagem

    # Encerra a conexão
    C_SOCKET.close()

if __name__ == "__main__":
    main()