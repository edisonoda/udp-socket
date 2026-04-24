from socket import *
import json

# ip = input('Insira o endereço IP: ')
# porta = int(input('Insira a porta do servidor: '))
ip = '127.0.0.1'
porta = 12000

# Cria o socket UDP (IPv4, Datagrama)
# AF_INET (Address Family - Internet)
# SOCK_DGRAM (Socket Datagram)
clientSocket = socket(AF_INET, SOCK_DGRAM)
server = (ip, porta)

def main():
    req = {'type': 'GET', 'msg': '/gatinho.gif', 'ack': 0}

    clientSocket.sendto(json.dumps(req).encode(), server)

    recebidos = []

    # simulação perda

    # recepção
    # verificar integridade segmentos
    # Aguarda resposta (buffer de 2048) e decodifica
    resp, addr = clientSocket.recvfrom(2048)
    print('Servidor:', resp.decode())
    recebidos.append(resp.decode())

    # montagem

    # Encerra a conexão
    clientSocket.close()

if __name__ == "__main__":
    main()