from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(200), nullable=False)
    principle = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    audio_path = db.Column(db.String(200), nullable=True)

    def __init__(self, book_title, principle, content, audio_path=None):
        self.book_title = book_title
        self.principle = principle
        self.content = content
        self.audio_path = audio_path
