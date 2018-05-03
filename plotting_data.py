
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import os
import re
import seaborn as sns


# pwd = "./" the main directory of peacock 
RESULTS_PATH = './results/'
DELIMITER  = r"\|"
# number of episodes
NUM_EPI = 300


epi_df = pd.read_csv(RESULTS_PATH + 'episode_data.csv',header = None )
cols = epi_df.shape[1]
epi_df['Combined'] = epi_df.loc[:,:].apply(lambda x: " ".join(x), axis =1)
epi_df['ConvergeEpi'] = epi_df.iloc[:, cols - 1].apply(lambda x: re.search(r"\d+",x).group()).astype(float)

def getInitialInfluencers(string):
	lt = []
	for match in re.finditer(DELIMITER, string):
	    lt.append(match.start())
	return string[lt[0]+ 1: lt[1]]

def getStableInfluencers(string):
	lt = []
	for match in re.finditer(DELIMITER, string):
	    lt.append(match.start())
	return string[lt[1]+ 1: lt[2]]	

epi_df["InitInfluencers"] = epi_df['Combined'].apply(getInitialInfluencers)
epi_df["InitInfluencers"] = epi_df["InitInfluencers"].apply(lambda x: x[1:len(x)-1])
epi_df["StableInfluencers"] = epi_df["Combined"].apply(getStableInfluencers)
epi_df['StableInfluencers'] = epi_df['StableInfluencers'].apply(lambda x: x[1:len(x)-1])

data_df = epi_df[['ConvergeEpi','InitInfluencers','StableInfluencers']]
del epi_df



# plt.figure(figsize=(15,10))
# ax= sns.barplot(data = data_df,palette = sns.cubehelix_palette(data_df.shape[0]))
# plt.xlabel('influencers')
# plt.ylabel('episodes to converge')
# plt.title('group epi')
# plt.savefig("all.png")


gp = data_df.groupby(['StableInfluencers'])['InitInfluencers'].count().reset_index()
gp.sort_values('StableInfluencers',ascending = False)
fig, ax = plt.subplots(figsize=(15,7))
gp.plot(ax = ax)
fig.autofmt_xdate()
fig.savefig("all.png")







