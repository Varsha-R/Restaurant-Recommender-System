import pandas as pd

def recommend_on_cuisines(selected_cuisines):
	df = pd.read_csv('C:\\Users\\Nalina Vadmal\\Documents\\zomato_qualified_restaurants.csv')
	nested_list = []
	for i in range(0, len(selected_cuisines)):
		list_rest = []
		for j in range(0, 4042):
			if selected_cuisines[i] in df.iloc[j]['cuisines']:
				dataframe = {}
				dataframe['rest_name'] = df.iloc[j]['rest_name']
				dataframe['locality'] = df.iloc[j]['locality']
				dataframe['cost_for_two'] = df.iloc[j]['cost_for_two']
				dataframe['rating'] = df.iloc[j]['rating']
				dataframe['votes'] = df.iloc[j]['votes']
				dataframe['score'] = df.iloc[j]['score']
				dataframe['cuisines'] = df.iloc[j]['cuisines']
				list_rest.append(dataframe)
		df1 = pd.DataFrame(list_rest)
		df1 = df1.head(7)
		nested_list.append(df1)
	return nested_list

def cuisine_recommendations(title, titles, indices, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    rest_indices = [i[0] for i in sim_scores]
    final = titles.iloc[rest_indices].head(6)
    return final.values

def content_based_recommender(user, titles, indices, cosine_sim):
	df_restaurants = pd.read_csv('C:\\Users\\Nalina Vadmal\\Documents\\zomato_restaurants.csv')
	df_non_rec = pd.read_csv('C:\\Users\\Nalina Vadmal\\Documents\\content_based_non_rec.csv')
	final = []
	l = len(user)
	for i in range(0, l):
		list_of_recommendation = []
		if user[i]['rest_name'] in df_non_rec['rest_name'].values or user[i]['rest_name'] not in df_restaurants['rest_name'].values:
			continue
		else:
			if(df_restaurants.loc[df_restaurants['rest_name'] == user[i]['rest_name']]['rating'].iloc[0] > 3.0):
				list_of_recommendation = cuisine_recommendations(user[i]['rest_name'], titles, indices, cosine_sim)
				for i in range(0, len(list_of_recommendation)):
					dataframe = {}
					dataframe['rest_name'] = list_of_recommendation[i]
					dataframe['rating'] = float(df_restaurants.loc[df_restaurants['rest_name'] == dataframe['rest_name']]['rating'].values[0])
					final.append(dataframe)
	return final

def collaborative_filtering_recommender(username):
	userR = pd.read_csv('C:\\Users\\Nalina Vadmal\\Documents\\userRatings.csv')
	corrM = pd.read_csv('C:\\Users\\Nalina Vadmal\\Documents\\corrMatrix.csv')
	user_index = userR.cust_name[userR.cust_name == username].index[0]
	myRatings = userR.iloc[user_index].dropna()
	simCandidates = pd.Series()
	for i in range(1, len(myRatings.index)):
		sims = corrM[myRatings.index[i]].dropna()
		sims = sims.map(lambda x: x * myRatings[i])
		simCandidates = simCandidates.append(sims)
	simCandidates.sort_values(inplace=True, ascending=False)
	myRatings = myRatings[1:]
	filteredSims = simCandidates.drop(myRatings.index, errors='ignore')
	l = len(filteredSims)
	indexes = simCandidates.index.values
	final = []
	for i in range(0, l):
		dataframe = {}
		dataframe['rest_name'] = corrM['rest_name'][indexes[i]]
		final.append(dataframe)
	return final