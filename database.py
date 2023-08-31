import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database():
    def __init__(self, nome):
        self.conn= sqlite3.connect(str(nome)+'.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL)")

    def add(self, note):
        self.cur.execute(f"INSERT INTO note (title, content) VALUES ('{note.title}','{note.content}')")
        self.conn.commit()
    
    def get_all(self):
        notes=[]
        cursor = self.conn.execute("SELECT id,title,content FROM note")
        for linha in cursor:
            note=Note(id=linha[0],title=linha[1],content=linha[2])
            notes.append(note)
        return notes
    
    def update(self, entry):
        self.cur.execute(f"UPDATE note SET title = '{entry.title}' , content = '{entry.content}' WHERE id= {entry.id}")
        self.conn.commit()

    def delete(self, note_id):
        self.cur.execute(f"DELETE FROM note WHERE id = {note_id}")
        self.conn.commit()


