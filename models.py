"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

MAX_STR_LEN = 50
MAX_NOTE_LEN = 5000

class Cupcake(db.Model):
    """Cupcake."""

    __tablename__ = "cupcakes"

    def __repr__(self):
        return f"""<cake id={self.id} flavor={self.flavor} size={self.size} image={self.image}
                rating={self.rating}>"""

    id = db.Column(db.Integer, # int not the same as SQL Integer, the ORM translates etween python and postgreSQL
                    primary_key=True,
                    autoincrement=True)
    
    flavor = db.Column(db.String(MAX_STR_LEN),
                            nullable=False)

    size = db.Column(db.String(MAX_STR_LEN),
                            nullable=False)

    rating = db.Column(db.Float,
                        nullable=False)


    image = db.Column(db.String(MAX_NOTE_LEN), 
                        nullable=False,
                        default='https://tinyurl.com/demo-cupcake')


    def serialize_cupcake(self):
        """serialize cupcakes"""
        
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image" : self.image
        }
    

