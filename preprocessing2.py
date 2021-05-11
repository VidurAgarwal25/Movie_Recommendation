#%%
import numpy as np
import pandas as pd

# %%
credits = pd.read_csv('Dataset/credits.csv')
# %%
credits
# %%
meta = pd.read_csv('Dataset/movies_metadata.csv')
# %%
meta

# %%
meta['release_date'] = pd.to_datetime(meta['release_date'], errors='coerce')

# %%
meta['year'] = meta['release_date'].dt.year

# %%
meta
# %%
meta['year'].value_counts().sort_index()
# %%
# Getting only 2017 movies as we already have movies up to the year 2016 in preprocessing 1 file. 
# We don't have enough data for the movies from 2018, 2019 and 2020. 
new_meta = meta.loc[meta.year == 2017,['genres','id','title','year']]

# %%
new_meta
# %%
new_meta['id'] = new_meta['id'].astype(int)
# %%
data = pd.merge(new_meta, credits, on='id')

# %%
data
# %%
#strings have python expressions like dictionary in this case so we are using it to traverse it easily
import ast
data['genres'] = data['genres'].map(lambda x: ast.literal_eval(x))
data['cast'] = data['cast'].map(lambda x: ast.literal_eval(x))
data['crew'] = data['crew'].map(lambda x: ast.literal_eval(x))
# %%
def make_genresList(x):
    gen = []
    st = " "
    for i in x:
        if i.get('name') == 'Science Fiction':
            scifi = 'Sci-Fi'
            gen.append(scifi)
        else:
            gen.append(i.get('name'))
    if gen == []:
        return np.NaN
    else:
        return (st.join(gen))
# %%
data['genres_list'] = data['genres'].map(lambda x: make_genresList(x))
# %%
data['genres_list']
# %%
def get_actor1(x):
    casts = []
    for i in x:
        casts.append(i.get('name'))
    if casts == []:
        return np.NaN
    else:
        return (casts[0])
# %%
data['actor_1_name'] = data['cast'].map(lambda x: get_actor1(x))
# %%
def get_actor2(x):
    casts = []
    for i in x:
        casts.append(i.get('name'))
    if casts == [] or len(casts)<=1:
        return np.NaN
    else:
        return (casts[1])
# %%
data['actor_2_name'] = data['cast'].map(lambda x: get_actor2(x))
# %%
def get_actor3(x):
    casts = []
    for i in x:
        casts.append(i.get('name'))
    if casts == [] or len(casts)<=2:
        return np.NaN
    else:
        return (casts[2])
# %%
data['actor_3_name'] = data['cast'].map(lambda x: get_actor3(x))
# %%
def get_directors(x):
    dt = []
    st = " "
    for i in x:
        if i.get('job') == 'Director':
            dt.append(i.get('name'))
    if dt == []:
        return np.NaN
    else:
        return (st.join(dt))

# %%
data['director_name'] = data['crew'].map(lambda x: get_directors(x))
# %%
movie = data.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres_list','title']]
# %%
movie
# %%
movie.isna().sum()
# %%
movie = movie.dropna(how='any')
# %%
movie.isna().sum()
# %%
movie = movie.rename(columns={'genres_list':'genres'})
movie = movie.rename(columns={'title':'movie_title'})
# %%
movie['movie_title'] = movie['movie_title'].str.lower()
# %%
movie['comb'] = movie['actor_1_name'] + ' ' + movie['actor_2_name'] + ' '+ movie['actor_3_name'] + ' '+ movie['director_name'] +' ' + movie['genres']
# %%
old = pd.read_csv('data.csv')
# %%
old['comb'] = old['actor_1_name'] + ' ' + old['actor_2_name'] + ' '+ old['actor_3_name'] + ' '+ old['director_name'] +' ' + old['genres']
# %%
new = old.append(movie)
# %%
#dataset of movies upto 2017
new
# %%
#If movie title is repeating then we are deleting the duplicates 
new.drop_duplicates(subset ="movie_title", keep = 'last', inplace = True)
# %%
new.to_csv('main_data.csv',index=False)
# %%
