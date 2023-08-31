import os
import json

def extract_route(request):
    oi=request.split("/n")
    t=oi[0]
    response=t.split(" ")
    final=response[1]

    return final[1:]

def read_file(Path):

    with open(Path, mode='rb') as file:
        conteudo=file.read()
        return conteudo

def load_data(ar_json):
    with open('data/' + ar_json, 'r') as arquivo:
        return json.load(arquivo)
    
def load_template(nome_arquivo):
    with open('templates/' + nome_arquivo, 'r') as arquivo:
        return arquivo.read()
    
def recebe(dicionario):
    with open("data/notes.json", "r") as data:
        notas=json.load(data)
    
    notas.append(dicionario)
    with open("data/notes.json", "w") as dat:
       dat.write(json.dumps(notas, indent=4))
    
def build_response(body='', code='200', reason='OK', headers=''):
    print("*************",headers)
    response= f'HTTP/1.1 {code} {reason}\n'
    if headers:
        response += headers+'\n'
    response+= '\n'+ str(body)
    return response.encode()