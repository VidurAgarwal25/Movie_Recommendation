#%%
import pandas as pd
import numpy as np
# %%
data = pd.read_csv('Dataset/movie_metadata.csv')
# %%
data.head(10)
# %%
data.shape
# %%
import matplotlib.pyplot as plt
data.title_year.value_counts(dropna=False).sort_index().plot(kind='barh',figsize=(15,16))
plt.show()
# %%
data = data.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']]
# %%
data['actor_1_name'] = data['actor_1_name'].replace(np.nan, 'unknown')
data['actor_2_name'] = data['actor_2_name'].replace(np.nan, 'unknown')
data['actor_3_name'] = data['actor_3_name'].replace(np.nan, 'unknown')
data['director_name'] = data['director_name'].replace(np.nan, 'unknown')

# %%
data

# %%
data['genres'] = data['genres'].str.replace('|', ' ')
# %%
data['movie_title'] = data['movie_title'].str.lower()
# %%
data['movie_title'] = data['movie_title'].apply(lambda x : x[:-1])
# %%
data.to_csv('data.csv',index=False)
# %%
