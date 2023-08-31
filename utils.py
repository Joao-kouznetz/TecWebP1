import os
import json

from database import Database
from database import Note 

db = Database('banco')

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

def load_data():
    dados_transformados=[]
    notes = db.get_all()
    for i in notes:
        titulo=i.title
        titulo=titulo.replace("+"," ")
        conteudo=i.content
        conteudo=conteudo.replace("+"," ")
        dados_transformados.append({'titulo':titulo, 'detalhes':conteudo})
    return dados_transformados
    
    
def load_template(nome_arquivo):
    with open('templates/' + nome_arquivo, 'r') as arquivo:
        return arquivo.read()
    
def adiciona_note(dicionario):
    db.add(Note(title=dicionario['titulo'], content=dicionario['detalhes']))
    
def build_response(body='', code='200', reason='OK', headers=''):
    print("*************",headers)
    response= f'HTTP/1.1 {code} {reason}\n'
    if headers:
        response += headers+'\n'
    response+= '\n'+ str(body)
    return response.encode()