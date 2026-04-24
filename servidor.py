from socket import *
import json
import threading

controle_clientes = {}

# Segmentação: Dividir o arquivo em múltiplos segmentos/pedaços para envio em datagramas UDP.
def separar_seg(caminho_arq, addr_chave, tamanho_arq=512):
    with open(caminho_arq, 'rb') as f:
        segmento = f.read(tamanho_arq)
        if not segmento:
            return False
        
        controle_clientes[addr_chave]['segmento'] = segmento
        return segmento

def verificar_ack(caminho_arq, addr_chave, ack):
    cliente = controle_clientes[addr_chave]

    if cliente['ack'] == ack:
        serverSocket.sendto(cliente['segmento'], cliente['addr'])
    else:
        serverSocket.sendto(separar_seg(caminho_arq, addr_chave), cliente['addr'])
    
    cliente['timer'].start()

def main():
    # Cria o socket UDP (IPv4, Datagrama)
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    # Porta: número maior que 1024
    # Fixa a porta (’’ escuta em todas as interfaces de rede)
    serverSocket.bind(('', 12000))
    print('Servidor pronto para receber pacotes...')

    while True:
        # Aguardar conexões/mensagens de clientes.
        # Bloqueia e aguarda pacote. Salva dados e IP/Porta de origem
        msg, addr = serverSocket.recvfrom(2048)
        msg = json.loads(msg)
        # print(json.loads(msg)['ack'])
        print(addr)
        addr_chave = f'{addr[0]}:{addr[1]}'
        
        if addr_chave not in controle_clientes:
            controle_clientes[addr_chave] = {
                'addr': addr,
                'timer': threading.Timer(2.0, verificar_ack(msg['msg'], addr_chave, msg['ack']))
            }  

        controle_clientes[addr_chave]['ack'] = msg['ack']
        print(controle_clientes[addr_chave]['ack'])

        controle_clientes[addr_chave]['timer'].cancel()    

        # Verificar se o arquivo solicitado existe.
        # Se o arquivo não existir: Enviar uma mensagem de erro claramente definida pelo seu protocolo para o cliente.
        # arquivo = requisição !!!
        # if arquivo nao existe:
            # serverSocket.sendto('Erro: arquivo solicitado não existe'.encode(), addr)
        # else:
        # for data in segmentar_arquivo(arquivo, 4096):
        #     process(data)
            # serverSocket.sendto(data.encode(), addr)

        
        # Retransmissão: Implementar lógica para reenviar segmentos específicos caso o cliente solicite (devido a perdas ou erros).
        
        # Regra de negocio: converte texto para maiusculas
        mod_msg = 'oi'
        # Envia resposta de volta usando o endereco capturado
        serverSocket.sendto(mod_msg.encode(), addr)

if __name__ == "__main__":
    main()