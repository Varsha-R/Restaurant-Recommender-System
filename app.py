import pandas as pd
from flask import Flask, render_template, request
from pymongo import MongoClient
import quiz_recommendations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

# Homepage
@app.route('/')
def homepage():
    return render_template('index.html')

# Quiz questions landing page
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/recommendations', methods=['POST'])
def display_recommendations():
    selected_cuisines = request.form.getlist('selected_cuisine')
    recommendations = quiz_recommendations.recommend_on_cuisines(selected_cuisines)
    return render_template('display_recommendations.html', zipped=zip(selected_cuisines, recommendations))

@app.route('/signin')
def login():
	return render_template('signin.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method=="POST":
       username = request.form['username']
       user_collection = collection.find({'cust_name': username})
       user = list(user_collection)
       if not user:
           message = "Oops! Looks like you haven't rated any restaurants :"
           return render_template('oops.html', message=message)
       else:
           df = pd.read_csv('C:\\Users\\Nalina Vadmal\\Documents\\zomato_restaurants.csv')
           df['cuisines'] = df['cuisines'].fillna("").astype('str')
           tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
           tfidf_matrix = tf.fit_transform(df['cuisines'])
           cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
           titles = df['rest_name']
           indices = pd.Series(df.index, index=df['rest_name'])
           final_recommendations = quiz_recommendations.content_based_recommender(user, titles, indices, cosine_sim)
           if(len(final_recommendations)==0):
               message = "Sorry! We don't have any recommendations for you"
               return render_template('oops.html', message=message)
           else:
               return render_template('find_similar.html', user=user, final_recommendations=final_recommendations)

@app.route('/sup_signin')
def login_superuser():
	return render_template('superuser_signin.html')

@app.route('/superuser', methods=['POST'])
def superuser_predict():
    if request.method=="POST":
       username = request.form['username']
       user_collection = collection.find({'cust_name': username})
       user = list(user_collection)
       if not user:
           message = "Oops! Looks like you haven't rated any restaurants :"
           return render_template('oops.html', message=message)
       else:
           if len(user) <= 3:
               message = "Sorry! You don't have superuser status :"
               return render_template('oops.html', message=message)
           else:
               final_rec = quiz_recommendations.collaborative_filtering_recommender(username)
               if(len(final_rec)==0):
                   message = "Sorry! We don't have any recommendations for you"
                   return render_template('oops.html', message=message)
               else:
                   return render_template('superuser_recommendations.html', final_rec=final_rec, user=user)

if __name__ == "__main__":
    uri = "mongodb://127.0.0.1:27017"
    client = MongoClient(uri)
    database = client['RestaurantRecommender']
    collection = database['user_ratings']
    app.run(port=5000, debug=True)
