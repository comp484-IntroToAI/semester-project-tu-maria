import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecipeRecommender:
    def __init__(self):
        self.user_profile = {
            "allergies": [],
            "excluded_ingredients": []
        }
        self.api_key = 'd044bf9007d3494a89ad987cb83c2e64'  

    def get_user_ingredients(self):
        # Prompt the user for ingredients they want to include
        ingredients_input = input("Enter the ingredients you want (comma-separated): ")
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(',')]
        return ingredients



    def update_user_profile(self):
        # Ask the user if they want to add allergies or excluded ingredients
        add_ingredients = input(
            "Do you want to add allergies or excluded ingredients? (type 'allergies' or 'excluded'): ").lower()

        if add_ingredients == 'allergies':
            allergies_input = input("Enter your allergies (comma-separated): ")
            allergies = [allergy.strip() for allergy in allergies_input.split(',')]
            self.user_profile['allergies'] = allergies
        elif add_ingredients == 'excluded':
            excluded_input = input("Enter the ingredients you want to exclude (comma-separated): ")
            excluded_ingredients = [excluded.strip() for excluded in excluded_input.split(',')]
            self.user_profile['excluded_ingredients'] = excluded_ingredients

        # Ask the user for desired ingredients
        ingredients = self.get_user_ingredients()  # Get the desired ingredients from the user
        self.user_profile['desired_ingredients'] = ingredients  # Add to the user profile

        print(f"Updated user profile: {self.user_profile}")

    def extract_ingredients(self, user_input):
        # Clean and return the ingredients
        ingredients = user_input.lower().split(' and ')
        return ingredients

    def fetch_recipe_details(self, recipe_id):
        """Fetch detailed recipe information using the recipe ID."""
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            recipe_data = response.json()
            # Extract recipe details: name, image, ingredients, and cooking instructions
            title = recipe_data.get('title')
            image = recipe_data.get('image')
            ingredients = [ingredient['originalString'] for ingredient in recipe_data.get('extendedIngredients', [])]
            instructions = recipe_data.get('instructions', 'No instructions available.')

            return title, image, ingredients, instructions
        else:
            print(f"Error fetching details for recipe {recipe_id}")
            return None

    def search_recipes(self, ingredients):
        query = ','.join(ingredients)
        exclude_query = ','.join(self.user_profile["excluded_ingredients"])

        url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={self.api_key}&includeIngredients={query}&excludeIngredients={exclude_query}&number=10&fillIngredients=false'

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

    def filter_recipes_by_similarity(self, all_recipes, ingredients):
        excluded = set(self.user_profile["excluded_ingredients"])
        valid_recipes = []

        for recipe in all_recipes:
            used_ingredients = set(ingredient['name'] for ingredient in recipe.get('usedIngredients', []))
            print(f"Used ingredients for recipe {recipe['title']}: {used_ingredients}")

            if not excluded.intersection(used_ingredients):  # Only keep recipes without excluded ingredients
                valid_recipes.append(recipe)

        if not valid_recipes:
            print("No recipes without excluded ingredients.")
            return []

        recipe_ingredients = [
            " ".join([ingredient['name'] for ingredient in recipe.get('usedIngredients', [])])
            for recipe in valid_recipes
        ]

        print(f"Valid recipe ingredients: {recipe_ingredients}")

        if not any(recipe_ingredients):
            print("No valid ingredients found in recipes.")
            return []

        tfidf = TfidfVectorizer(stop_words=None)
        tfidf_matrix = tfidf.fit_transform(recipe_ingredients)

        user_tfidf_profile = tfidf.transform([" ".join(ingredients)])

        cosine_similarities = cosine_similarity(user_tfidf_profile, tfidf_matrix).flatten()

        for i, recipe in enumerate(valid_recipes):
            recipe['similarity_score'] = cosine_similarities[i]

        sorted_recipes = sorted(valid_recipes, key=lambda x: x['similarity_score'], reverse=True)

        return sorted_recipes

    def display_recipe_info(self, recipes):
        """Display the name, image, ingredients, and instructions of each recipe."""
        for recipe in recipes:
            title = recipe.get('title')
            image = recipe.get('image')
            recipe_id = recipe.get('id')

            # Fetch additional details (ingredients and instructions)
            title, image, ingredients, instructions = self.fetch_recipe_details(recipe_id)

            print(f"Recipe: {title}")
            print(f"Image: {image}")
            print(f"Ingredients: {', '.join(ingredients)}")
            print(f"Instructions: {instructions}")
            print("-" * 40)




    def get_recipe_details(self, recipe_id):
        url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={self.api_key}'

        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching recipe details from Spoonacular API")
            return None

    def get_random_recipe(self):
        url = f'https://api.spoonacular.com/recipes/random?apiKey={self.api_key}&number=1'

        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('recipes', [])[0]  # Returns the first random recipe
        else:
            print("Error fetching random recipe from Spoonacular API")
            print("Status Code:", response.status_code)
            print("Response:", response.json())
            return None




    def display_recipe(self, recipe_details):
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
            print(recipe_details.get('instructions') or "No instructions")


# Create an instance of RecipeRecommender
recommender = RecipeRecommender()

# Update user profile
recommender.update_user_profile()

# Extract ingredients from user input
ingredients = recommender.extract_ingredients("chicken, broccoli")

# Search for recipes based on ingredients
recipes = recommender.search_recipes(ingredients)

# Filter recipes by similarity (based on ingredients)
filtered_recipes = recommender.filter_recipes_by_similarity(recipes, ingredients)

# Display the top recipe details
if filtered_recipes:
    recipe_details = recommender.get_recipe_details(filtered_recipes[0]['id'])
    recommender.display_recipe(recipe_details)
