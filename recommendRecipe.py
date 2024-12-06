import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean


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
            title = recipe_data.get('title', 'No title available')
            image = recipe_data.get('image', 'No image available')
            ingredients = [
                f"{ingredient.get('amount', 0)} {ingredient.get('unit', '')} {ingredient.get('name', 'Unknown ingredient')}"
                for ingredient in recipe_data.get('extendedIngredients', [])
            ]
            instructions = recipe_data.get('instructions', 'No instructions available.')
            calories = next((item for item in recipe_data.get('nutrition', {}).get('nutrients', [])
                             if item.get('title') == 'Calories'), {}).get('amount', None)
            return title, image, ingredients, instructions, calories
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
            if results:
                return results
            else:
                print("No recipes found with the given ingredients and exclusions.")
                return self.handle_no_matches(ingredients)
        else:
            print("Error fetching data from Spoonacular API")
            return []

    def handle_no_matches(self, ingredients):
        # Identify the last ingredient in the search
        last_ingredient = ingredients[-1]
        print(f"Finding similar ingredient for: {last_ingredient}")

        # Fetch all ingredients in the database
        all_ingredients = self.get_all_ingredients()
        if not all_ingredients:
            print("No available ingredients to compare for similarity.")
            return []

        # Calculate similarity to the last ingredient based on nutritional values
        similar_ingredient = self.find_most_similar_ingredient(last_ingredient, all_ingredients)

        if similar_ingredient:
            print(f"Replacing {last_ingredient} with similar ingredient: {similar_ingredient}")
            # Replace the last ingredient with the most similar one
            ingredients[-1] = similar_ingredient
            # Reattempt the recipe search
            return self.search_recipes(ingredients)
        else:
            print("No similar ingredient found.")
            return []



    def get_all_ingredients(self):
        all_ingredients = set()
        page = 1
        max_pages = 10  # Limit API calls for safety
        endpoint = f'https://api.spoonacular.com/recipes/complexSearch'

        while page <= max_pages:
            url = f"{endpoint}?apiKey={self.api_key}&number=100&offset={100 * (page - 1)}"
            response = requests.get(url)

            if response.status_code == 200:
                recipes = response.json().get('results', [])
                for recipe in recipes:
                    recipe_id = recipe.get('id')
                    details = self.fetch_recipe_details(recipe_id)
                    if details:
                        _, _, ingredients, _, _ = details
                        for ingredient in ingredients:
                            ingredient_name = ingredient.split()[-1]
                            all_ingredients.add(ingredient_name.lower())
            else:
                print(f"Error fetching recipes on page {page}. Status Code: {response.status_code}")
                break

            page += 1

        return list(all_ingredients)

    def find_most_similar_ingredient(self, target_ingredient, all_ingredients):
        """Find the most nutritionally similar ingredient to the target ingredient."""
        if target_ingredient not in self.ingredient_nutrition:
            print(f"No nutritional data for {target_ingredient}")
            return None

        target_nutrition = np.array([self.ingredient_nutrition[target_ingredient].get(key, 0)
                                     for key in ['calories', 'protein', 'fat', 'carbs']])
        min_distance = float('inf')
        most_similar = None

        for ingredient in all_ingredients:
            nutrition = self.ingredient_nutrition.get(ingredient)
            if not nutrition:
                continue

            ingredient_vector = np.array([nutrition.get(key, 0) for key in ['calories', 'protein', 'fat', 'carbs']])
            distance = euclidean(target_nutrition, ingredient_vector)

            if distance < min_distance:
                min_distance = distance
                most_similar = ingredient

        return most_similar



    def get_all_ingredients(self):
        """
        Fetch all unique ingredients by aggregating them from a large set of recipes.
        """
        all_ingredients = set()  # Use a set to avoid duplicates
        page = 1
        max_pages = 10  # Adjust based on API limits or desired number of recipes
        endpoint = f"{self.base_url}/recipes/complexSearch"

        while page <= max_pages:
            url = f"{endpoint}?apiKey={self.api_key}&number=100&offset={100 * (page - 1)}"
            response = requests.get(url)

            if response.status_code == 200:
                recipes = response.json().get('results', [])
                for recipe in recipes:
                    recipe_id = recipe.get('id')
                    details = self.fetch_recipe_details(recipe_id)
                    if details:
                        _, _, ingredients, _, _ = details
                        for ingredient in ingredients:
                            ingredient_name = ingredient.split()[-1]  # Simplify to ingredient name
                            all_ingredients.add(ingredient_name.lower())
            else:
                print(f"Error fetching recipes on page {page}. Status Code: {response.status_code}")
                break

            page += 1

        return list(all_ingredients)

    def calculate_ingredient_nutrients(self, ingredients):
        total_nutrients = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}

        for ingredient in ingredients:
            ingredient_data = self.ingredient_nutrition.get(ingredient.lower())
            if ingredient_data:
                for key in total_nutrients:
                    total_nutrients[key] += ingredient_data.get(key, 0)
        return total_nutrients


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
        for recipe in recipes:
            title = recipe.get('title')
            image = recipe.get('image')
            recipe_id = recipe.get('id')

            # Fetch additional details (ingredients and instructions)
            title, image, ingredients, instructions, _ = self.fetch_recipe_details(recipe_id)

            print(f"Recipe: {title}")
            print(f"Image: {image}")
            print(f"Ingredients: {', '.join(ingredients)}")
            print(f"Instructions: {instructions}")
            print("-" * 40)

    def get_random_recipe(self):
        url = f'https://api.spoonacular.com/recipes/random?apiKey={self.api_key}&number=1'

        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('recipes', [])[0]
        else:
            print("Error fetching random recipe from Spoonacular API")
            print("Status Code:", response.status_code)
            print("Response:", response.json())
            return None

    def display_recipe(self, recipe_details):
        if recipe_details:
            title, image, ingredients, instructions, _ = recipe_details

            print(f"\nRecipe: {title}")
            print(f"Image: {image}")
            print(f"\nIngredients:")
            for ingredient in ingredients:
                print(f" - {ingredient}")

            print("\nInstructions:")
            print(instructions)
        else:
            print("No recipe details available.")


if __name__ == "__main__":
    recommender = RecipeRecommender()

    # Gather user inputs
    ingredients = input("Enter ingredients you have (comma-separated): ").split(",")
    recommender.user_profile["excluded_ingredients"] = input("Enter ingredients to exclude (comma-separated): ").split(",")
    recommender.user_profile["diet"] = input("Enter diet preference (e.g., vegetarian, vegan, etc. or leave blank): ")

    # Search for recipes
    print("\nSearching for recipes...\n")
    recipes = recommender.search_recipes(ingredients)

    # Display the first result
    if recipes:
        first_recipe = recipes[0]
        print(f"Showing the first recipe: {first_recipe.get('title', 'No title available')} (ID: {first_recipe.get('id')})")
        recipe_id = first_recipe["id"]
        recipe_details = recommender.fetch_recipe_details(recipe_id)
        recommender.display_recipe(recipe_details)
    else:
        print("No recipes found.")

