from config import db

class Movie(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(50), unique=False, nullable=False)
    year=db.Column(db.String(10), unique=False, nullable=False)
    director=db.Column(db.String(50), unique=True, nullable=False)
    
    def to_json(self):
        return{
            "id":self.id,
            "title": self.title,
            "year": self.year,
            "director":self.director,
        }
    
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), unique=False, nullable=False)
        
    def to_json(self):
        return{
            "id":self.id,
            "username": self.username,
        }
    
class Comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    comment= db.Column(db.String(200), nullable=False)
        
    def to_json(self):
        return{
            "id": self.id,
            "userId": self.user_id,
            "movieId": self.movie_id,
            "comment": self.comment
        }
        
