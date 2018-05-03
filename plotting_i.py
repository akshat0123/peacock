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


def read_file(seq,path):
	return pd.read_csv(path + 'episode_{}.csv'.format(seq),header = None )

def getLastInfluencer(string):
	posi_start = re.search(DELIMITER, string).start()
	return string[:posi_start - 1]

def getGenTweets(string):
	posi_start = re.search(DELIMITER, string).start()
	return string[posi_start + 1:]

def strip_index(string):
	posi_start = re.search(DELIMITER, string).start()
	return string[posi_start + 2 :]
def get_numberEpi(string):
	return re.match(r"[0-9]", string).group()

for i in range(NUM_EPI):

# needs to be modified 
	epi_df = read_csv(i,RESULTS_PATH)
	cols = epi_df.shape[1]

	epi_df.iloc[:,0] = epi_df.iloc[:,0].apply(strip_index) 

	epi_df['LastInfluencer'] = epi_df.iloc[:,cols - 1].apply(getLastInfluencer) 
	epi_df['GenTweets'] = epi_df.iloc[:,cols - 1].apply(getGenTweets)

	epi_df.drop( epi_df.columns[cols-1], axis =1, inplace = True)

	epi_df['InfluencersGroup'] = epi_df.loc[:,:"LastInfluencer"].apply(lambda x: "".join(x), axis =1)



	fig, ax = plt.subplots(figsize=(15,7))
	epi_df.groupby(['InfluencersGroup'])['GenTweets'].count().plot(ax = ax)



fig.autofmt_xdate()
fig.savefig("test.png")


















