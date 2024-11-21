import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Function to clean and extract ingredients from user input
def extract_ingredients(user_input):
    # Clean and return the ingredients
    ingredients = user_input.lower().split(' and ')
    return ingredients


# Function to search for recipes on Spoonacular
def search_recipes(ingredients):
    api_key = 'd044bf9007d3494a89ad987cb83c2e64'  # Use your API key here
    query = ','.join(ingredients)
    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&includeIngredients={query}&number=10&fillIngredients=false'

    response = requests.get(url)
    print(f"API Response: {response.json()}")  # Add this line to check the response

    if response.status_code == 200:
        results = response.json().get('results', [])
        if not results:
            print("No recipes found with the given ingredients. Try adjusting your input.")
        return results
    else:
        print("Error fetching data from Spoonacular API")
        return []

# Function to filter recipes using content-based filtering (TF-IDF + Cosine Similarity)
def filter_recipes_by_similarity(all_recipes, ingredients):
    # Extract the ingredients and prepare a list of recipe ingredients
    recipe_ingredients = []
    for recipe in all_recipes:
        # Check if there are any usedIngredients
        used_ingredients = [ingredient['name'] for ingredient in recipe.get('usedIngredients', [])]

        if used_ingredients:  # Only add recipes that have ingredients
            recipe_ingredients.append(" ".join(used_ingredients))

    if not recipe_ingredients:
        print("No recipes with valid ingredients found.")
        return []

    # Create a TF-IDF vectorizer to compare ingredient sets
    tfidf = TfidfVectorizer(stop_words='english')

    try:
        tfidf_matrix = tfidf.fit_transform(recipe_ingredients)
    except ValueError as e:
        print(f"Error during TF-IDF transformation: {e}")
        return []

    # Create a user profile based on input ingredients
    user_profile = tfidf.transform([" ".join(ingredients)])

    # Compute cosine similarity between user input and each recipe's ingredients
    cosine_similarities = cosine_similarity(user_profile, tfidf_matrix).flatten()

    # Add similarity score to the recipes
    for i, recipe in enumerate(all_recipes):
        recipe['similarity_score'] = cosine_similarities[i]

    # Sort recipes by similarity score in descending order
    sorted_recipes = sorted(all_recipes, key=lambda x: x['similarity_score'], reverse=True)

    return sorted_recipes


# Function to get detailed recipe information
def get_recipe_details(recipe_id):
    api_key = 'd044bf9007d3494a89ad987cb83c2e64'  # Replace with your Spoonacular API key
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching recipe details from Spoonacular API")
        return None


# Function to get a random recipe
def get_random_recipe():
    api_key = 'd044bf9007d3494a89ad987cb83c2e64'  # Replace with your Spoonacular API key
    url = f'https://api.spoonacular.com/recipes/random?apiKey={api_key}&number=1'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('recipes', [])[0]  # Returns the first random recipe
    else:
        print("Error fetching random recipe from Spoonacular API")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        return None


# Function to display the recipe with full details
def display_recipe(recipe_details):
    if recipe_details:
        print(f"\nRecipe: {recipe_details['title']}")
        print(f"Image: {recipe_details['image']}")
        print(
            f"Recipe URL: https://spoonacular.com/recipes/{recipe_details['id']}-{recipe_details['title'].replace(' ', '-').lower()}")
        print("\nIngredients:")

        for ingredient in recipe_details.get('extendedIngredients', []):
            name = ingredient['name']
            amount = ingredient['amount']
            unit = ingredient['unit']
            print(f" - {amount} {unit} {name}")

        print("\nInstructions:")
        print(recipe_details.get('instructions') or "No instructions available.")
    else:
        print("Could not retrieve recipe details.")


# Main function to display either a recipe based on ingredients or a random recipe
def display_best_recipe(user_input):
    if user_input.lower() == "random" or not user_input.strip():
        print("Fetching a random recipe for you...")
        recipe_details = get_random_recipe()
        display_recipe(recipe_details)
    else:
        ingredients = extract_ingredients(user_input)  # Extract ingredients from user input
        recipes = search_recipes(ingredients)  # Search recipes matching the ingredients

        if recipes:
            # Get details of the first recipe
            best_recipe = recipes[0]
            recipe_details = get_recipe_details(best_recipe['id'])
            display_recipe(recipe_details)
        else:
            print("Sorry, no recipes found for your request.")


# Example usage
user_input = input("What do you want to cook? (e.g., chicken and rice or type 'random' for any recipe): ")
display_best_recipe(user_input)