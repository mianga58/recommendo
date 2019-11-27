import pandas as pd
import numpy as np
# libraries for making count matrix and similarity matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# reading the data from the preprocessed .csv file
data = pd.read_csv('data.csv')

# making the new column containing combination of all the features
data['comb'] = data['Sub_1']+' '+ data['Sub_2']+' '+ data['Sub_3']+' '+ data['Sub_4']+' '+ data['school']+' '+ data['Sum']


# creating a count matrix
cv = CountVectorizer()
count_matrix = cv.fit_transform(data['comb'])

# creating a similarity score matrix
sim = cosine_similarity(count_matrix)

# saving the similarity score matrix in a file for later use
np.save('similarity_matrix', sim)

# saving dataframe to csv for later use in main file
data.to_csv('data.csv',index=False)