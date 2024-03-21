from flask import request, jsonify #will allow us to return JSON data
from config import app, db
from models import User, Movie, Comment

# type of request: get(access), post (create), patch(update) and delete

@app.route("/movies_list", methods=["GET"])
def movies_list():
    # get all the different movies from the database
    movies=Movie.query.all()
    # we must to return a JSON data, so we have to convert the python object
    json_movies=list(map(lambda x: x.to_json(), movies))
    return  jsonify({"movies":json_movies})

# getting the data associated and submit JSON data
@app.route("/add_movie", methods=["POST"])
def add_movie():
    title=request.json.get("title")
    year=request.json.get("year")
    director=request.json.get("director")
    
    # verify if the variables are valid or not; if not, show a message
    if not title or not year or not director:
       return(
            jsonify({"message":"You must include all information"}), 400,
       ) 

    # construct a new Contact object
    new_movie = Movie(title=title, year=year, director=director)
    # and add to my database
    try:
        db.session.add(new_movie)
        db.session.commit()
    except Exception as e:   
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message": "Movie added!"}), 201

@app.route("/update_movie/<int:movie_id>", methods=["PATCH"])
def update_movie(movie_id):
    # get the contact from the database
    movie=Movie.query.get(movie_id)
    # if don't find the expecific movie it'll send a message
    if not movie:
       return jsonify({"message":"Movie not found"}), 404
   
    # get the new data from JSON and keep it in variables
    data=request.json
    movie.title=data.get("title", movie.title)
    movie.year=data.get("year", movie.year)
    movie.director=data.get("director", movie.director)

    db.session.commit()
    
    return jsonify({"message": "Movie updated"}),200

@app.route("/delete_movie/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    # get contact from database
    movie=Movie.query.get(movie_id)
   
    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    
    db.session.delete(movie)
    db.session.commit()
    
    return jsonify({"message": "Movie deleted"}), 200
   
@app.route("/users_list", methods=["GET"])
def users_list():
    # get all the different movies from the database
    users=User.query.all()
    # we must to return a JSON data, so we have to convert the python object
    json_users=list(map(lambda x: x.to_json(), users))
    return  jsonify({"users":json_users})

@app.route("/add_user", methods=["POST"])
def add_user():
    username=request.json.get("username")
    
    if not username:
       return(
            jsonify({"message":"You must include an username"}), 400,
       ) 

    # construct a new Contact object
    new_user = User(username=username)
    # and add to my database
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:   
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message": "User created!"}), 201

@app.route("/update_user/<int:user_id>", methods=["PATCH"])
def update_username(user_id):
    # get the contact from the database
    user=User.query.get(user_id)
    # if don't find the expecific movie it'll send a message
    if not user:
       return jsonify({"message":"User not found"}), 404
   
    # get the new data from JSON and keep it in variables
    data=request.json
    user.username=data.get("username", user.username)
    
    db.session.commit()
    
    return jsonify({"message": "User updated"}),200

@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # get contact from database
    user=User.query.get(user_id)
   
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted"}), 200
 
@app.route("/movie_comments_list/<int:movie_id>", methods=["GET"])
def movie_comments_list(movie_id):
    movie_comments=Comment.query.filter_by(movie_id=movie_id).all()
    
    json_movie_comments=list(map(lambda x: x.to_json(), movie_comments))
    return  jsonify({"movie_comments":json_movie_comments})

@app.route("/user_comments_list/<int:user_id>", methods=["GET"])
def user_comments_list(user_id):
    user_comments=Comment.query.filter_by(user_id=user_id).all()
    
    json_user_comments=list(map(lambda x: x.to_json(), user_comments))
    return  jsonify({"user_comment":json_user_comments})

@app.route("/add_comment/<int:movie_id>/<int:user_id>", methods=["POST"])
def add_comment(movie_id, user_id):
    comment=request.json.get("comment")
       
    if not comment:
       return(
            jsonify({"message":"You must include a comment"}), 400,
       ) 

    new_comment = Comment(movie_id=movie_id, user_id=user_id, comment=comment)
    
    try:
        db.session.add(new_comment)
        db.session.commit()
    except Exception as e:   
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message": "Comment added!"}), 201



        
if __name__=="__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)