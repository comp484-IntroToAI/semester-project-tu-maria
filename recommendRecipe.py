import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecipeRecommender:
    def __init__(self):
        self.user_profile = {
            "excluded_ingredients": [],
            "diet": None
        }
        self.api_key = 'd044bf9007d3494a89ad987cb83c2e64'

    def fetch_recipe_details(self, recipe_id):
        """Fetch detailed recipe information using the recipe ID."""
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            recipe_data = response.json()

            # Extract recipe details
            title = recipe_data.get('title', 'No title available')
            image = recipe_data.get('image', 'No image available')
            # Handle missing keys
            ingredients = [
                f"{ingredient.get('amount', 0)} {ingredient.get('unit', '')} {ingredient.get('name', 'Unknown ingredient')}"
                for ingredient in recipe_data.get('extendedIngredients', [])
            ]
            instructions = recipe_data.get('instructions', 'No instructions available.')

            return title, image, ingredients, instructions
        else:
            print(f"Error fetching details for recipe {recipe_id}, Status Code: {response.status_code}")
            return None

    def search_recipes(self, ingredients):
        query = ','.join(ingredients)
        exclude_query = ','.join(self.user_profile["excluded_ingredients"])
        diet_query = self.user_profile["diet"]

        url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={self.api_key}&includeIngredients={query}&excludeIngredients={exclude_query}&number=10&fillIngredients=false'

        if diet_query:
            url += f"&diet={diet_query}"

        response = requests.get(url)
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
            if not excluded.intersection(used_ingredients):  # Only keep recipes without excluded ingredients
                valid_recipes.append(recipe)

        if not valid_recipes:
            print("No recipes without excluded ingredients.")
            return []

        recipe_ingredients = [
            " ".join([ingredient['name'] for ingredient in recipe.get('usedIngredients', [])])
            for recipe in valid_recipes
        ]

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
            title, image, ingredients, instructions = recipe_details

            print(f"\nRecipe: {title}")
            print(f"Image: {image}")
            print(f"\nIngredients:")
            for ingredient in ingredients:
                print(f" - {ingredient}")

            print("\nInstructions:")
            print(instructions)
        else:
            print("No recipe details available.")


# test
# if __name__ == "__main__":
#     recommender = RecipeRecommender()
#
#     recommender.user_profile["excluded_ingredients"] = ["peanuts", "eggplant"]
#     recommender.user_profile["diet"] = "vegetarian"
#
#     search_ingredients = ["tomato", "cheese", "basil"]
#     recipes = recommender.search_recipes(search_ingredients)
#
#     if recipes:
#         print(f"Found {len(recipes)} recipes. Displaying the first one:\n")
#         first_recipe_details = recommender.fetch_recipe_details(recipes[0]['id'])
#         recommender.display_recipe(first_recipe_details)
#     else:
#         print("No recipes found.")