import hashlib

# Padronização das ações:
# - GET arquivo.ext
# - DATA seq checksum bytes
# - (N)ACK seq
# - ERROR
# - END

def checksum(data):
    return hashlib.md5(data).hexdigest()

def parse_msg(msg):
    parts = msg.split(b' ', 3)
    if not parts:
        return None, None
    
    # 0: ação, 1-N: outros argumentos
    return parts[0], parts[1:]