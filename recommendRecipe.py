import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_recipes(df, user_diet, user_avoid_ingredient, user_preferences):
    """
    Recommends recipes based on diet preference, ingredients to avoid, and similarity to user's preferred ingredients.

    """

    # Step 1: Filter recipes to only keep those matching the diet preference
    filtered_recipes = df[df['diet'] == user_diet]

    # Step 2: Filter recipes to exclude those containing the unwanted ingredient
    filtered_recipes = filtered_recipes[~filtered_recipes['ingredients'].str.contains(user_avoid_ingredient, case=False)]

    # Step 3: Vectorize ingredients using TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(filtered_recipes['ingredients'])

    # Step 4: Create user profile based on preferred ingredients
    user_profile = tfidf.transform([user_preferences])

    # Step 5: Calculate cosine similarities between user profile and each recipe
    cosine_similarities = cosine_similarity(user_profile, tfidf_matrix).flatten()

    # Step 6: Add similarity score to the filtered recipes DataFrame
    filtered_recipes = filtered_recipes.copy()
    filtered_recipes['similarity_score'] = cosine_similarities

    # Step 7: Sort recipes by similarity score in descending order
    recommended_recipes = filtered_recipes.sort_values(by='similarity_score', ascending=False)

    return recommended_recipes[['recipe_id', 'ingredients', 'similarity_score']]

# Sample recipe data
data = {
    'recipe_id': [1, 2, 3, 4],
    'ingredients': [
        'tomato basil pasta',
        'spinach cheese pasta',
        'chicken tomato basil',
        'pasta garlic tomato'
    ],
    'diet': ['vegetarian', 'vegetarian', 'non-vegetarian', 'vegetarian']
}
df = pd.DataFrame(data)

# User preferences
user_diet = "vegetarian"
user_avoid_ingredient = "garlic"
user_preferences = "basil tomato pasta"

# Get recommended recipes
recommended_recipes = recommend_recipes(df, user_diet, user_avoid_ingredient, user_preferences)

# Print recommended recipes
print(recommended_recipes)
