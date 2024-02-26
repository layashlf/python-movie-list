from flask import Blueprint, render_template, request, redirect, url_for, flash,g,make_response,session
from my_app.controllers.database import open_connection,close_connection

moviesBp = Blueprint('movies', __name__, url_prefix='/movies')


@moviesBp.route('/', methods=['GET', 'POST'])
def list():
    """
    This Python function retrieves a list of movies from a database and renders them in an HTML
    template.
    :return: a rendered template 'movies/movies.html' with the data from the movie_list. The movie_list
    is a list of dictionaries containing information about movies retrieved from the database table
    'movies'. Each dictionary in the movie_list represents a movie record with keys 'id', 'title',
    'description', 'created_at', 'completed_at', and 'poster'.
    """
    if request.method=="GET":
        movie_list=[]
        try:
            db_obj = open_connection()
            cursor = db_obj.cursor(buffered=True)
            query = "select * from movies"
            cursor.execute(query)
            movies = cursor.fetchall()

            for (id,title,description,created_at,completed_at,poster) in movies:
                movie_list.append({'id':id,
                                   "title":title,
                                   "description":description,
                                   "created_at":created_at,
                                   "completed_at":completed_at,
                                   "poster":poster
                                   })
            cursor.close()
        finally:
            close_connection()
        return render_template('movies/movies.html',data=movie_list)


@moviesBp.route('/list', methods=('GET',))
def myPlaylist():
    """
    This Python function retrieves a user's playlist of movies from a database and renders them in a
    template for display.
    :return: The function `myPlaylist()` is returning a rendered template 'movies/myPlaylist.html' with
    the data extracted from the database query. The data being returned is a list of dictionaries, where
    each dictionary represents a movie in the playlist. Each dictionary contains the following keys:
    'id', 'title', 'movies_id', 'description', 'created_at', 'completed_at', 'poster', 'p_id
    """
    if request.method=="GET":
        movie_list=[]
        try:
            db_obj = open_connection()
            cursor = db_obj.cursor(buffered=True)
            query = "SELECT  m.*,p.id as p_id,p.user_id FROM movies m JOIN playlist p ON m.id = p.movie_id WHERE p.user_id = %s"
            cursor.execute(query,(session['user']['user_id'],))
            movies = cursor.fetchall()

            for (movie_id,title,description,created_at,completed_at,poster,p_id,user_id) in movies:
                movie_list.append({"id":id,
                                   "title":title,
                                   "movies_id":movie_id,
                                   "description":description,
                                   "created_at":created_at,
                                   "completed_at":completed_at,
                                   "poster":poster,
                                   "p_id":p_id,
                                   "user_id":user_id,
                                   })


            cursor.close()
        finally:
            close_connection()
        return render_template('movies/myPlaylist.html',data=movie_list)


@moviesBp.route('/add/<movie_id>', methods=('GET', ))
def add(movie_id=None):
    """
    The `add` function inserts a movie into a user's playlist in a database and redirects to the movies
    list page, handling errors and displaying appropriate messages.
    
    :param movie_id: The `add` function you provided seems to be a Python function for adding a movie to
    a playlist in a database. It takes a `movie_id` as a parameter
    :return: The `make_response(redirect(url_for('movies.list'))) ` is being returned.
    """

    if(movie_id is not None):
        success=True

        try:
            user_id=session['user']['user_id']


            db_obj = open_connection()
            cursor = db_obj.cursor()
            query = "INSERT INTO playlist (user_id, movie_id) VALUES ( %s, %s)"
            cursor.execute(
                query,
                (user_id,movie_id),
            )
            cursor.close()
            db_obj.commit()
            message = 'Added successfully'
        except:
            message = 'something went wrong'
            success=False
        finally:
            close_connection()
            flash({'success':success,"message":message})
            return make_response(redirect(url_for('movies.list')))



@moviesBp.route('/remove/<playlist_id>', methods=('GET', 'POST'))
def remove(playlist_id=None):
    """
    The function `remove` deletes a playlist entry from the database based on the provided `playlist_id`
    and returns a success message or an error message.
    
    :param playlist_id: The `remove` function you provided seems to be a Python function for removing a
    playlist entry from a database. It takes a `playlist_id` as a parameter to identify which playlist
    entry to remove
    :return: a response using the `make_response` function, which redirects the user to a specific route
    based on the condition. If `playlist_id` is not provided, it redirects to the login route. If
    `playlist_id` is provided and the deletion is successful, it redirects to the `myPlaylist` route.
    """

    if(playlist_id is not None):
        message=None
        success=True
        try:
            user_id=session['user']['user_id']


            db_obj = open_connection()
            cursor = db_obj.cursor()
            query = "DELETE FROM playlist where user_id =  %s and id = %s"
            cursor.execute(
                query,
                (user_id,playlist_id),
            )
            cursor.close()
            db_obj.commit()
            message="Removed successfully"
        except:
            success=False
            message="something went wrong! Please try again"

        finally:

            close_connection()
            flash({"success":success ,"message":message})

            return make_response(redirect(url_for('movies.myPlaylist')))


    return make_response(redirect(url_for('auth.login')))




