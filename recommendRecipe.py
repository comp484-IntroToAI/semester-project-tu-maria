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
        self.ingredient_nutrition = {
            'tomato': {'calories': 22, 'protein': 1.1, 'fat': 0.2, 'carbs': 4.8},
            'cheese': {'calories': 113, 'protein': 7.1, 'fat': 9.3, 'carbs': 0.4},
            'basil': {'calories': 5, 'protein': 0.5, 'fat': 0.1, 'carbs': 1.0},
            # Add more ingredients with their nutritional data here
        }

    def fetch_recipe_details(self, recipe_id):
        """Fetch detailed recipe information using the recipe ID."""
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            recipe_data = response.json()

            # Extract recipe details
            title = recipe_data.get('title', 'No title available')
            image = recipe_data.get('image', 'No image available')
            ingredients = [
                f"{ingredient.get('amount', 0)} {ingredient.get('unit', '')} {ingredient.get('name', 'Unknown ingredient')}"
                for ingredient in recipe_data.get('extendedIngredients', [])
            ]
            instructions = recipe_data.get('instructions', 'No instructions available.')
            nutrition = recipe_data.get('nutrition', {}).get('nutrients', [])
            calories = next((item for item in nutrition if item['title'] == 'Calories'), {}).get('amount', None)

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
            if not results:
                print("No recipes found with the given ingredients and exclusions.")
                # Proceed to calculate similarity based on nutrients and calories
                return self.search_recipes_by_nutritional_similarity(ingredients)
            return results
        else:
            print("Error fetching data from Spoonacular API")
            return []

    def search_recipes_by_nutritional_similarity(self, ingredients):
        # Fallback to search by nutritional similarity if no exact recipe found
        all_recipes = self.get_all_recipes()
        if not all_recipes:
            return []

        ingredient_profiles = []
        for recipe in all_recipes:
            title, image, recipe_ingredients, instructions, calories = self.fetch_recipe_details(recipe['id'])
            nutrient_values = self.calculate_ingredient_nutrients(recipe_ingredients)
            ingredient_profiles.append({
                'id': recipe['id'],
                'title': title,
                'calories': calories,
                'nutrients': nutrient_values
            })

        # Calculate Euclidean and Cosine similarity for each recipe
        user_nutrients = self.calculate_ingredient_nutrients(ingredients)
        ingredient_profiles = sorted(ingredient_profiles,
                                     key=lambda x: self.calculate_similarity(user_nutrients, x['nutrients']),
                                     reverse=True)

        return ingredient_profiles[:5]  # Return the top 5 recipes based on nutrient similarity

    def calculate_ingredient_nutrients(self, ingredients):
        total_nutrients = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}

        for ingredient in ingredients:
            ingredient_data = self.ingredient_nutrition.get(ingredient.lower())
            if ingredient_data:
                for key in total_nutrients:
                    total_nutrients[key] += ingredient_data.get(key, 0)
        return total_nutrients

    def calculate_similarity(self, user_nutrients, recipe_nutrients):
        euclidean_distance = self.calculate_euclidean_distance(user_nutrients, recipe_nutrients)
        cosine_distance = self.calculate_cosine_distance(user_nutrients, recipe_nutrients)

        return euclidean_distance + cosine_distance

    def calculate_euclidean_distance(self, user_nutrients, recipe_nutrients):
        user_vector = np.array([user_nutrients[key] for key in user_nutrients])
        recipe_vector = np.array([recipe_nutrients[key] for key in recipe_nutrients])
        return euclidean(user_vector, recipe_vector)

    def calculate_cosine_distance(self, user_nutrients, recipe_nutrients):
        user_vector = np.array([user_nutrients[key] for key in user_nutrients])
        recipe_vector = np.array([recipe_nutrients[key] for key in recipe_nutrients])
        return 1 - cosine_similarity([user_vector], [recipe_vector])[0][0]

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
            return response.json().get('recipes', [])[0]  # Returns the first random recipe
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

