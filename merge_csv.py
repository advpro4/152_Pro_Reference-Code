import csv

all_movies = []
link_list = []

csv_file_pointer = open('movies.csv' , 'r' , encoding = 'utf-8')
csv_file_reader = csv.reader(csv_file_pointer)
column_header = next(csv_file_reader)
# print(column_header , len(column_header))                                   # 27 columns

for movie in csv_file_reader:
    all_movies.append(movie)

# print(len(all_movies))                                                      # 4803

# close the file
csv_file_pointer.close()

# operating on movie_links file
file_object = open('movie_links.csv' , 'r' , encoding = 'utf-8')
file_data = csv.reader(file_object)
columns = next(file_data)
for movie in file_data:
    link_list.append(movie)

# close the file
file_object.close()

# print(len(link_list))                                                          # 4747


# checking if movie exists in link list
for movie in all_movies:
    movie_name = movie[8]                            # 8th element is original_title
    movie_link = ""

    for movie_data in link_list:
        if movie_name in movie_data:
            movie_link = movie_data[1]               # 0th item is movie name and 1st item is movie link
            break                                    # no need to iterate further

    movie.append(movie_link)                         # append movie_link to the movie list [Either link or empty]


# adding one more element to our header list
column_header.append('poster link')

# # printing to verify
# print(column_header)

# preparing the final dataset
csv_file_object = open('final.csv' , 'a+' , encoding = 'utf-8' , newline = '')     # opening file in append mode
csv_file_writer = csv.writer(csv_file_object)                                      # writer object
csv_file_writer.writerow(column_header)                                            # writing a row in a new file
for movie in all_movies:
    if len(movie)  ==  28:
        csv_file_writer.writerow(movie)

csv_file_object.close()                                                            # close the file

