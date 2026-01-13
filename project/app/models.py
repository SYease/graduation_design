from app import db
from datetime import datetime

class Algorithm(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    difficulty=db.Column(db.Float)
    created_at=db.Column(db.DateTime,default=datetime.now)

    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'difficulty':self.difficulty
        }
        

