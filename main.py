import csv
from flask import Flask , jsonify , request

# importing list of top_movies from demographic.py module
from demographic import top_movies

# importing get recommendation function from content_filtering.py module
from content_filtering import get_recommendations
from itertools import groupby

# opening file in read mode
file_pointer = open('movies.csv' , 'r' , encoding= 'utf-8')
file_data = csv.reader(file_pointer)
column_header = next(file_data)

all_movies = []
liked_movies = []
disliked_movies = []
did_not_watch_movies = []

# iterating through all the rows
# error after running this command
'''
Traceback (most recent call last):
  File "main.py", line 13, in <module>
    for movie in file_data:
  File "C:\Python37\lib\encodings\cp1252.py", line 23, in decode
    return codecs.charmap_decode(input,self.errors,decoding_table)[0]
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 4718: character maps to <undefined>
'''

for movie in file_data:
  movie_name = movie[8]
  all_movies.append(movie_name)

# print(all_movies , len(all_movies))

# once we have all the data, close the file
file_pointer.close()

# creating flask app
app = Flask(__name__)

# app routes and decorator functions
@app.route('/movies' , methods = ['GET'])
def get_movies():
  movie = all_movies[0]
  response = jsonify({'data' : movie , 'status' : 'success'})
  return response , 201

# like route, POST request : updating liked_movies list
@app.route('/like' , methods = ['POST'])
def like():
  global all_movies
  global liked_movies
  movie = all_movies[0]
  all_movies = all_movies[1:]
  liked_movies.append(movie)
  print('Liked movies : ' , liked_movies)
  response = jsonify({'status' : 'success'})
  return response , 201

# dislike route, POST request : updating disliked_movies list
@app.route('/dislike' , methods = ['POST'])
def dislike():
  global all_movies
  global disliked_movies
  movie = all_movies[0]
  all_movies = all_movies[1:]
  disliked_movies.append(movie)
  print('Disliked movies : ' , disliked_movies)
  response = jsonify({'status' : 'success'})
  return response , 201

# did not watch route, POST request : updating did_not_watch_movies list
@app.route('/did_not_watch' , methods = ['POST'])
def did_not_watch():
  global all_movies
  global did_not_watch_movies
  movie = all_movies[0]
  all_movies = all_movies[1:]
  did_not_watch_movies.append(movie)
  print('Did not watched movies : ' , did_not_watch_movies)
  response = jsonify({'status' : 'success'})
  return response , 201

# api for top rated movies : demographic filtered movies
@app.route('/popular_movies' , methods = ['GET'])
def popular_movies():
  top_rated_movies = []
  for movie in top_movies:
    d = {
      'title'         : movie[0],
      'link'          : movie[1],
      'duration'      : str(int(movie[2])) + ' minutes',
      'release date'  : movie[3],
      'rating'        : int(movie[4]),
      'overview'      : movie[5]
    }

    top_rated_movies.append(d)

  response = {'data' : top_rated_movies , 'status' : 'success'}
  return jsonify(response) , 201

# api for recommended movies using content based filtering
@app.route('/recommended_movies' , methods = ['GET'])
def recommended_movies():
    all_recommended_movies = []
    unique_data = []

    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie)
        all_recommended_movies.append(output)

    all_recommended_movies.sort()                              # removing duplicates, sort the movies first
    grouped_data = groupby(all_recommended_movies)
    for key , group in grouped_data:
      unique_data.append(key)

    recommended = []
    for movie in unique_data:
      d = {
        'title'         : movie[0],
        'link'          : movie[1],
        'duration'      : movie[2],
        'release date'  : movie[3],
        'rating'        : movie[4],
        'overview'      : movie[5]
      }

    recommended.append(d)

    response = {'data' : recommend , 'status' : 'success'}
    return jsonify(response) , 201

# running the app on local server
if __name__  ==  '__main__':
  app.run(debug = True)