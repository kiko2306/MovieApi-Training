from flask import request, jsonify #will allow us to return JSON data
from config import app, db
from models import User, Movie, Comment

# type of request: get(access), post (create), patch(update) and delete

#endpoint to see all movies of database
@app.route("/movies_list", methods=["GET"])
def movies_list():
    # get all the different movies from the database
    movies=Movie.query.all()
    # we must to return a JSON data, so we have to convert the python object
    #map function will apply lambda for each row in 'movies'
    json_movies=list(map(lambda x: x.to_json(), movies))
    return  jsonify({"movies":json_movies})

# enpoint to add a new movie in database
@app.route("/add_movie", methods=["POST"])
def add_movie():
    #we get information from JSON and keep it in a variable
    title=request.json.get("title")
    year=request.json.get("year")
    director=request.json.get("director")
    
    # verify if the variables are valid or not; if not, show a message
    if not title or not year or not director:
       return(
            jsonify({"message":"You must include all information"}), 400,
       ) 

    # construct a new Movie object
    new_movie = Movie(title=title, year=year, director=director)
    # and add to the database
    try:
        db.session.add(new_movie)
        db.session.commit()
    except Exception as e:   
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message": "Movie added!"}), 201

#endpoint to update the information about a movie
@app.route("/update_movie/<int:movie_id>", methods=["PATCH"])
def update_movie(movie_id):
    # get a specific movie from the database
    movie=Movie.query.get(movie_id)
    # if don't find the expecific movie it'll send a message
    if not movie:
       return jsonify({"message":"Movie not found"}), 404
   
    # get the data from JSON and update the values of the variables according JSON
    data=request.json
    movie.title=data.get("title", movie.title)
    movie.year=data.get("year", movie.year)
    movie.director=data.get("director", movie.director)

    # updating the database
    db.session.commit()
    
    return jsonify({"message": "Movie updated"}),200

#endpoint to delete informations about a movie
@app.route("/delete_movie/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    # get movie from database
    movie=Movie.query.get(movie_id)
    #check if the movie exist; if not return a message about
    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    #open the session database and delete the information there
    db.session.delete(movie)
    db.session.commit()
    
    return jsonify({"message": "Movie deleted"}), 200

# endpoint to see all users  
@app.route("/users_list", methods=["GET"])
def users_list():
    # get all the different users from the database
    users=User.query.all()
    # return a JSON data, so we have to convert the python object to JSON
    json_users=list(map(lambda x: x.to_json(), users))
    #print on the screen all information requested
    return  jsonify({"users":json_users})

# endpoint to add a new user
@app.route("/add_user", methods=["POST"])
def add_user():
    # get the information from JSON
    username=request.json.get("username")
    # check if the user exists, if not show a message
    if not username:
       return(
            jsonify({"message":"You must include an username"}), 400,
       ) 
    # construct a new User object
    new_user = User(username=username)
    # and add to the database
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:   
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message": "User created!"}), 201

# endpoint to update the user
@app.route("/update_user/<int:user_id>", methods=["PATCH"])
def update_username(user_id):
    # get a specific use from the database
    user=User.query.get(user_id)
    # if don't find the specific user it'll send a message
    if not user:
       return jsonify({"message":"User not found"}), 404
    # get the new data from JSON and keep it in variables
    data=request.json
    user.username=data.get("username", user.username)
    # save in database
    db.session.commit()
    
    return jsonify({"message": "User updated"}),200

# endpoint to delete an user and their comments
@app.route("/delete_user/<int:id>/<int:user_id_who_want_delete>", methods=["DELETE"])
def delete_user(id, user_id_who_want_delete):
    # get user information from database
    user=User.query.get(id)
    # check if the user exist, if not show a message
    if not user:
        return jsonify({"message": "User not found"}), 404
    # check who is trying to delete. Allow the process only if is the own user or adm (zero)
    if user.id==user_id_who_want_delete or user_id_who_want_delete==0:
        db.session.delete(user)
        # get all comments created by the user and delete
        comments_of_this_user= Comment.query.filter_by(user_id=id).all()
        for comment in comments_of_this_user:
            db.session.delete(comment)
    else:
        return jsonify({"message": "You don't have permission enough to delete an user"}), 401
    # save the database     
    db.session.commit()
    
    return jsonify({"message": "User deleted"}), 200

# endpoint to show all the comments about a specific movie
@app.route("/movie_comments_list/<int:movie_id>", methods=["GET"])
def movie_comments_list(movie_id):
    # get all comments about the movie
    movie_comments=Comment.query.filter_by(movie_id=movie_id).all()
    # convert to JSON
    json_movie_comments=list(map(lambda x: x.to_json(), movie_comments))
    # show the result of the query
    return  jsonify({"movie_comments":json_movie_comments})

#endpoint to show all the comments from a specific user
@app.route("/user_comments_list/<int:user_id>", methods=["GET"])
def user_comments_list(user_id):
    # get all comments from the user
    user_comments=Comment.query.filter_by(user_id=user_id).all()
    # convert to JSON
    json_user_comments=list(map(lambda x: x.to_json(), user_comments))
    # show the result of the query
    return  jsonify({"user_comment":json_user_comments})

# endpoint to add a comment about a movie / parameters: which movie is and who is posting the comment
@app.route("/add_comment/<int:movie_id>/<int:user_id>", methods=["POST"])
def add_comment(movie_id, user_id):
    # get a comment fro JSON
    comment=request.json.get("comment")
    # if not exist show a message
    if not comment:
       return(
            jsonify({"message":"You must include a comment"}), 400,
       ) 
    # create a new Comment object with all necessary information
    new_comment = Comment(movie_id=movie_id, user_id=user_id, comment=comment)
    # add and save in database
    try:
        db.session.add(new_comment)
        db.session.commit()
    except Exception as e:   
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message": "Comment added!"}), 201

# endpoint to update a comment / parameters: comment id and who is trying update the comment
@app.route("/update_comment/<int:id>/<int:user_id>", methods=["PATCH"])
def update_comment(id, user_id):
    # get the specific comment 
    comment_to_update=Comment.query.get(id)
    # validating the information
    if not comment_to_update:
            return jsonify({"message":"Comment not found"}), 404
    # check if who's trying to update is the same user that posted it
    if comment_to_update.user_id==user_id:
        # get the information from JSON and update it
        data=request.json
        comment_to_update.comment=data.get("comment", comment_to_update.comment)
    else:
        return jsonify({"message": "Only the user who posted this comment can update it!"}),200
    # save on database
    db.session.commit()
    
    return jsonify({"message": "Comment updated"}),200

# endpoint to delete a comment / parameters: comment id and who is trying delete the comment
@app.route("/delete_comment/<int:id>/<int:user_id>", methods=["DELETE"])
def delete_comment(id, user_id):
    # get the specific comment fro database
    comment_to_delete=Comment.query.get(id)
    # validate the information
    if not comment_to_delete:
        return jsonify({"message": "Comment not found"}), 404
    # check if who's trying to delete is the same user that posted it
    if comment_to_delete.user_id==user_id:
        db.session.delete(comment_to_delete)
        db.session.commit()
    else:
        return jsonify({"message": "Only the user who posted this comment can delete it!"}),401
    
    return jsonify({"message": "Comment deleted"}), 200

        
if __name__=="__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)