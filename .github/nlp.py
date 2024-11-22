import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


user_profile = {
        "allergies": [],
        "excluded_ingredients": []
    }

def update_user_profile():
    choice = input("Do you want to add allergies or excluded ingredients? (type 'allergies' or 'excluded'): ").strip().lower()
    if choice == "allergies":
        new_allergies = input("Enter your allergies (comma-separated): ").lower().split(',')
        user_profile["allergies"].extend([allergy.strip() for allergy in new_allergies])
    elif choice == "excluded":
        new_exclusions = input("Enter ingredients to exclude (comma-separated): ").lower().split(',')
        user_profile["excluded_ingredients"].extend([item.strip() for item in new_exclusions])
    else:
        print("Invalid choice. Please type 'allergies' or 'excluded'.")
    print("Updated user profile:", user_profile)




# Clean and extract ingredients from user input
def extract_ingredients(user_input):
    # Clean and return the ingredients
    ingredients = user_input.lower().split(' and ')
    return ingredients




# Search for recipes on Spoonacular
# Search for recipes on Spoonacular
def search_recipes(ingredients):

    api_key = 'd044bf9007d3494a89ad987cb83c2e64'  # Use your API key here
    query = ','.join(ingredients)
    exclude_query = ','.join(user_profile["excluded_ingredients"])  # Build exclude query from the user profile

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&includeIngredients={query}&excludeIngredients={exclude_query}&number=10&fillIngredients=false'

    response = requests.get(url)
    print(f"API Response: {response.json()}")  # Debugging
    if response.status_code == 200:
        results = response.json().get('results', [])
        if not results:
            print("No recipes found with the given ingredients and exclusions.")
        return results
    else:
        print("Error fetching data from Spoonacular API")
        return []


# Filter recipes using content-based filtering (TF-IDF + Cosine Similarity)
def filter_recipes_by_similarity(all_recipes, ingredients):
    excluded = set(user_profile["excluded_ingredients"])
    valid_recipes = []

    for recipe in all_recipes:
        used_ingredients = set(ingredient['name'] for ingredient in recipe.get('usedIngredients', []))
        if not excluded.intersection(used_ingredients):  # Only keep recipes without excluded ingredients
            valid_recipes.append(recipe)

    if not valid_recipes:
        print("No recipes without excluded ingredients.")
        return []

    # TF-IDF vectorizer to compare ingredient sets
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(recipe_ingredients)

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
while True:
    user_input = input("What do you want to cook? (e.g., 'chicken and rice', type 'random' for a random recipe, or 'profile' to update your preferences): ").strip().lower()

    if user_input == "profile":
        update_user_profile()
    elif user_input == "exit":
        print("Exiting the recipe recommender. Have a great day!")
        break
    else:
        display_best_recipe(user_input)
