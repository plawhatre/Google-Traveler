import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from sklearn.decomposition import PCA
import numpy as np
import urllib.parse
import os

def add_lat_lon(address):
  url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
  response = requests.get(url).json()
  if len(response)>0:
    return response[0]["lat"], response[0]["lon"]
  else:
    return None

def add_type(address):
  url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
  response = requests.get(url).json()
  if len(response)>0:
    return response[0]["type"]
  else:
    return None
  
def save_df_to_csv(df, city='city'):
    print(f"Runing function: {save_df_to_csv.__name__}")
    if not os.path.exists('./output'):
      os.mkdir('./output')
    df.to_csv('./output/' + city + '.csv', index=False)


def generate_df(url):
  """ collects attrations from google travel url for a city and generate a df
  """
  print(f"Runing function: {generate_df.__name__}")
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')

  city = soup.find('div', attrs={'class': 'kQb6Eb'})
  atractions = []
  notes = [] 
  ratings = []
  reviews = []

  for row in city.find_all_next('div', attrs={'class':'GwjAi'}): 

    # attractions
    atractions.append(row.find('div', attrs={'class': 'skFvHc YmWhbc'}).text)
    
    # notes
    notes.append(row.find('div', attrs={'class': 'nFoFM'}).text)
    
    # reviews and ratings
    temp = row.find('span', attrs={'class': 'ta47le'})
    try: 
      ratings.append(temp.text.split(' ')[0])
      reviews.append(re.sub('[\(, \)]', '', temp.text.split(' ')[-1]))
    except: 
      ratings.append(np.nan)
      reviews.append(np.nan)

  df = pd.DataFrame({'atractions': atractions, 'ratings': ratings, 'reviews': reviews, 'notes': notes})
  return df

def generate_combined_score(df):
  """Generate combined score after combining rating and reviews
  """
  print(f"Runing function: {generate_combined_score.__name__}")
  df['reviews'] = df['reviews'].astype(float)
  df['ratings'] = df['ratings'].astype(float)

  # df['reviews'].fillna(0, inplace=True)
  # df['ratings'].fillna(0, inplace=True)
  df = df.dropna()

  # 1: multiply rating and reviews
  df['cs_multiply'] = df['ratings'] * df['reviews']



  # 2: weighted sum of rating and reviews
  df['cs_weighted_sum'] = 0.7 * df['ratings'] + 0.3 * df['reviews']
  
  # 3: rank based combined score
  df['ratings_rank'] = df['ratings'].rank(ascending=False)
  df['reviews_rank'] = df['reviews'].rank(ascending=False)
  df['cs_rank'] = df['ratings_rank'] + df['reviews_rank']
  df = df.drop(['ratings_rank', 'reviews_rank'], axis=1) 

  # 4: geometric mean
  df['cs_gm'] = np.sqrt(df['ratings'] * df['reviews'])

  # 5: add rating and reviews after min-max scaling
  df['ratings_scaled'] = (df['ratings'] - df['ratings'].min()) / (df['ratings'].max() - df['ratings'].min())
  df['reviews_scaled'] = (df['reviews'] - df['reviews'].min()) / (df['reviews'].max() - df['reviews'].min())
  df['cs_add_scaled'] = df['ratings_scaled'] + df['reviews_scaled']
  df = df.drop(['ratings_scaled', 'reviews_scaled'], axis=1)


  # 6: Borda count
  ratings_rank = df['ratings'].rank(ascending=False)
  reviews_rank = df['reviews'].rank(ascending=False)
  borda_count = ratings_rank + reviews_rank
  df['cs_borda_count'] = np.max(borda_count) - borda_count + 1

  # 7: pca
  X = df[['ratings', 'reviews']]
  pca = PCA(n_components=1)
  pca.fit(X)
  X_pca = pca.transform(X)
  df['cs_pca'] = X_pca

  return df

def predict_categories(df, city):
  """ Use nominatim for categorization
  """
  print(f"Runing function: {predict_categories.__name__}")
  df['category'] = df.atractions.apply(lambda x: add_type(x+', '+city))

  return df

def combined_score_aggregation(df, method='borda'):
  """ Generate final rank
  """
  print(f"Runing function: {combined_score_aggregation.__name__}")
  if method == 'borda':
    scores = df.filter(regex=r'^cs_').apply(lambda x: x.rank(ascending=False))
    df['final_rank'] = scores.sum(axis=1).rank(ascending=True)

  elif method == 'copeland':
    scores = df.filter(regex=r'^cs_')
    wins = np.zeros((scores.shape[0], scores.shape[0]))
    for i in range(scores.shape[0]):
        for j in range(scores.shape[0]):
            wins[i,j] = sum(scores.iloc[i,:] > scores.iloc[j,:])
    losses = scores.shape[1] - wins - np.diag(np.ones(scores.shape[0]))
    df['final_rank'] = (wins - losses).sum(axis=1)
    df['final_rank'] = df['final_rank'].rank(ascending=False)
    
  else:
    raise ValueError(f"""Enter valid method : {method}\n
                         Enter one of the method from list
                         ['borda', 'copeland']""")

  return df.sort_values(by=['final_rank'])

def generate_location(df, city):
  print(f"Runing function: {generate_location.__name__}")
  df['location'] = df.atractions.apply(lambda x: add_lat_lon(x+', '+city))
  return df