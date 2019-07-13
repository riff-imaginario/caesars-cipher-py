import requests
import json
import hashlib


# variaveis que devem ser tratadas como constantes
endereco_api = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=e200ee778193b58fe467b60ca2277ce505028531'
resposta_api = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=e200ee778193b58fe467b60ca2277ce505028531'
arquivo_resposta = 'answer.json'


# request do json da codenation
msgCN = requests.get(endereco_api)


# Salvando mensagem no arquivo
with open(arquivo_resposta, 'w') as file:
    json.dump(msgCN.json(), file)

# Lendo arquivo
with open(arquivo_resposta, 'r') as f:
    msg = json.load(f)

cifra = msg['cifrado'].lower()
casas = int(msg['numero_casas'])

# Decifrando
aux = []

for letra in cifra:
    if letra.isalpha():
        if (ord(letra) - casas) < ord('a'):
            aux.append(chr((ord(letra) - casas) + 26))
        else:
            aux.append(chr(ord(letra) - casas))
    else:
        aux.append(letra)

msg_decifrada = ''.join(aux)

# Salvando mensagem decifrada
with open(arquivo_resposta, 'w') as file:
    msg['decifrado'] = msg_decifrada
    msg['resumo_criptografico'] = hashlib.sha1(msg_decifrada.encode('utf-8')).hexdigest()
    json.dump(msg, file)

# Enviando mensagem decifrada para API
answer = {'answer': open(arquivo_resposta, 'r')}
response = requests.post(resposta_api, files=answer)

print(response.status_code)