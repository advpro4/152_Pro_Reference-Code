import pandas as pd

# create a dataframe using final.csv file
df = pd.read_csv('final.csv')

# To calculate weighted average, we need R,v,C,m
R = df['vote_average']
v = df['vote_count']
C = df['vote_average'].mean()
m = df['vote_count'].quantile(0.9)
# print(C , m)                          # 6.092171559442016 , 1838.4000000000015

# adding weighted average col
df['weighted_rating'] = (R*v + C*m) / (v + m)
# print(df[['original_title' , 'weighted_rating']].head())

# sorting dataframe : wrt to weighted rating col in ascending order
df = df.sort_values('weighted_rating' , ascending = False)
# print(df[['original_title' , 'weighted_rating']].head())

# getting top 20 movies according to this descending order
top_movies = df[['original_title' , 'poster link' , 'runtime', 
                 'release_date' , 'weighted_rating' , 
                 'overview']].head(20).values.tolist()