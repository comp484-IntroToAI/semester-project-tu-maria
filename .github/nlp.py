import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample recipe data
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

# User preferences
user_diet = "vegetarian"   # Diet preference
user_avoid_ingredient = "garlic"  # Ingredient to avoid

# Step 1: Filter recipes based on dietary preference
filtered_recipes = df[df['diet'] == user_diet]

# Step 2: Remove recipes containing the unwanted ingredient
filtered_recipes = filtered_recipes[~filtered_recipes['ingredients'].str.contains(user_avoid_ingredient, case=False)]

# Step 3: Vectorize the ingredients text for the filtered recipes using TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(filtered_recipes['ingredients'])

# Step 4: User profile based on liked ingredients (you can modify the user preferences as needed)
user_preferences = "basil tomato pasta"
user_profile = tfidf.transform([user_preferences])

# Step 5: Calculate cosine similarity between user profile and each recipe
cosine_similarities = cosine_similarity(user_profile, tfidf_matrix).flatten()

# Step 6: Attach similarity scores to the filtered recipes DataFrame
filtered_recipes = filtered_recipes.copy()  # Make a copy to avoid modifying the original DataFrame
filtered_recipes['similarity_score'] = cosine_similarities

# Step 7: Sort recipes by similarity score in descending order
recommended_recipes = filtered_recipes.sort_values(by='similarity_score', ascending=False)


print(data)
print(recommended_recipes[['recipe_id', 'ingredients', 'similarity_score']])
