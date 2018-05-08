
# coding: utf-8

# In[1]:


import googlemaps
import pandas as pd
import numpy as np


# In[2]:


school = "國立政治大學"
gmap = googlemaps.Client('AIzaSyBGtdxA8CTLl7pyJDATrzVqpjs6InC1rbs')
gmap


# In[3]:


geo_result = gmap.geocode( school )
loc = geo_result[0]['geometry']['location']
loc


# In[4]:


restaurant =  gmap.places_radar( keyword='飲料店', location=loc, radius=1000 )
restaurant_rlt = restaurant['results']
len( restaurant_rlt )


# In[6]:


ids = list()
for place in restaurant_rlt :
	ids.append( place['place_id'] )
    
info = list()
for id in list(set(ids)) :
	info.append( gmap.place(place_id=id,language='zh-TW')['result'] )
    


# In[7]:


output = pd.DataFrame.from_dict(info)


# In[8]:


output


# In[9]:


latMap = lambda x:  x['location']['lat']
lngMap = lambda x:  x['location']['lng']
data = np.array(output.geometry)
tmp = np.vectorize(latMap)
tmp2 = np.vectorize(lngMap)
output['lat'] = tmp(data)
output['lng'] = tmp2(data)
output


# In[10]:


output.to_csv('drink.csv', encoding='utf-8')

