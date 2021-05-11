#%%
import pandas as pd
import numpy as np
import cgi
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# %%
df = pd.read_csv("main_data.csv")
# %%
features = ['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']
# %%
def combine_features(row):
    return row['director_name']+" "+row['actor_1_name']+" "+row['actor_2_name']+" "+row['genres']+" "+row['movie_title']

# %%
for feature in features:
    df[feature] = df[feature].fillna('') #filling all NaNs with blank string

df["combined_features"] = df.apply(combine_features,axis=1) #applying combined_features() method over each rows of dataframe and storing the combined string in "combined_features" column
# %%
df.iloc[0].combined_features
# %%
cv = CountVectorizer() #creating new CountVectorizer() object
count_matrix = cv.fit_transform(df["combined_features"]) #feeding combined strings(movie contents) to CountVectorizer() object
# %%
cosine_sim = cosine_similarity(count_matrix)
# %%
p=df.index.values
# %%
df.insert(0,column="index",value=p)
#%%
str1=""
# %%
def get_title_from_index(index):
    return df[df.index == index]["movie_title"].values[0]
def get_index_from_title(movie_title):
    return df[df.movie_title == movie_title]["index"].values[0]
#%%
from flask import Flask, render_template, request
import pickle
import cgi
import numpy as np

app = Flask('MOVIE_RECOMMENDATION')
@app.route('/')
def show_predict_stock_form():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
      #write your function that loads the model
      #model = get_model() #you can use pickle to load the trained model
      if request.method=='POST':

          movie_t = request.form['movie_title']
          print(movie_t)
          movie_user_likes = movie_t
          movie_user_likes=movie_user_likes.lower()
          movie_index = get_index_from_title(movie_user_likes)
          similar_movies = list(enumerate(cosine_sim[movie_index]))
          sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
          str1=" "
          i=1
          for element in sorted_similar_movies:
              str1+=get_title_from_index(element[0])+", "
              i=i+1
              if i>5:
                  break
          print(str1)
          return render_template('result.html', movie_title=movie_t,   predicted_movies=str1)

     

# %%
if __name__ == "__main__":
    app.run(debug=True)
# %%
