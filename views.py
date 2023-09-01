from utils import load_data, load_template, adiciona_note, build_response
from database import Database
from database import Note 
db = Database('banco')
import  urllib.parse
import re

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {
        }
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            item=chave_valor.split("=")
            # itens=chave_valor.split("=")
            item[1]=urllib.parse.unquote_plus(item[1], encoding='utf-8', errors='replace')
            params[item[0]]=item[1]
        adiciona_note(params)
        return build_response(code=303, reason='See Other', headers='Location: /')




    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados['titulo'], details=dados['detalhes'], id=dados['id'])
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)
   
    return build_response(body=load_template('index.html').format(notes=notes))

def delete(request):
    route_parts = request.split(' ')
    card_id = int(route_parts[1][7:])  # Extract the ID from the route

    # Remove the card with the specified ID from the database
    db.delete(card_id)

    return build_response(code=303, reason='See Other', headers='Location: /')

def paginaedit(request,route):
    card_id = route[4:]
    print(card_id, "---------------------------------------")
    todos=db.get_all()
    titulo='titulo'
    conteudo='conteudo'
    for note in todos:
        print(note.id, 'note_____id')
        print(card_id, 'card---id')
        if int(note.id)==int(card_id):
            print('entrou')
            titulo=note.title
            conteudo=note.content
    print('titulo',titulo)
    print('conteudo',conteudo)
    return build_response(body=load_template('edit.html').format(titulo=titulo, conteudo=conteudo))

def update(request,route):
    request = request.replace('\r', '')  # Remove caracteres indesejados
    # Cabeçalho e corpo estão sempre separados por duas quebras de linha
    partes = request.split('\n\n')
    corpo = partes[1]
    params = {
    }
    # Preencha o dicionário params com as informações do corpo da requisição
    # O dicionário conterá dois valores, o título e a descrição.
    # Posteriormente pode ser interessante criar uma função que recebe a
    # requisição e devolve os parâmetros para desacoplar esta lógica.
    # Dica: use o método split da string e a função unquote_plus
    id_match = route[4:] 
    for chave_valor in corpo.split('&'):
        item=chave_valor.split("=")
        # itens=chave_valor.split("=")
        item[1]=urllib.parse.unquote_plus(item[1], encoding='utf-8', errors='replace')
        params[item[0]]=item[1]
    params['id']=id_match
    entry={'title': params['titulo'], 'content': params['detalhes'] , 'id': params['id'] }
    db.update(entry)
    return build_response(code=303, reason='See Other', headers='Location: /')

def home():
    return build_response(code=303, reason='See Other', headers='Location: /')