import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# example recipe data
data = {
    'recipe_id': [1, 2, 3, 4],
    'ingredients': [
        'tomato basil pasta',         # Recipe 1, con
        'spinach cheese pasta',       # Recipe 2
        'chicken tomato basil',       # Recipe 3, contains meat
        'pasta garlic tomato'         # Recipe 4, contains garlic
    ],
    'diet': ['vegetarian', 'vegetarian', 'non-vegetarian', 'vegetarian']
}
df = pd.DataFrame(data)

# user preferences
user_diet = "vegetarian"   # example diet preference
user_avoid_ingredient = "garlic"  # example ngredient to avoid

## the user pref section will be modified once i can actually see the api data

# pt1, filter recipes to only keep diet pref
filtered_recipes = df[df['diet'] == user_diet]

# pt2, filter recipes to remove unwanted ingredients
filtered_recipes = filtered_recipes[~filtered_recipes['ingredients'].str.contains(user_avoid_ingredient, case=False)]

# pt3, vectorize ingredients using tf-idf ( Term Frequency-Inverse Document Frequency)
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(filtered_recipes['ingredients'])

# pt4, create user profile based on preffered ingredients
user_preferences = "basil tomato pasta"
user_profile = tfidf.transform([user_preferences])

#pt5, calculate cosin similarities
cosine_similarities = cosine_similarity(user_profile, tfidf_matrix).flatten()

#pt6, add score to df
filtered_recipes = filtered_recipes.copy()  # Make a copy to avoid modifying the original DataFrame
filtered_recipes['similarity_score'] = cosine_similarities

# Step 7: Sort recipes by similarity score in descending order
#pt7, sort, rank, and print the recipes
recommended_recipes = filtered_recipes.sort_values(by='similarity_score',
                                                   ascending=False)


print(data)
print(recommended_recipes[['recipe_id', 'ingredients', 'similarity_score']])
