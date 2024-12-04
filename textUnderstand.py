import spacy

class TextUnderstanding:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Define the intents with associated keywords
        self.intents = {
            "greet": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
            "search_information": ["ingredient", "nutrition", "calories", "fat", "protein", "carbohydrates", "vitamins"],
            "request_recipe": ["recipe", "cook", "make", "prepare", "dish", "meal"],
            "specify_allergies": ["allergy", "allergies", "allergic", "without", "no", "free", "intolerance", "sensitive", "avoid"],
        }
        
        # Diet-related keywords
        self.diet_keywords = [
            "gluten free", "ketogenic", "vegetarian", "lacto-vegetarian", "ovo-vegetarian", 
            "vegan", "pescetarian", "paleo", "primal", "low fodmap", "whole30"
        ]
        
        # Allergy-related keywords
        self.allergy_keywords = ["allergy", "allergic", "without", "no", "free", "intolerance", "sensitive", "avoid"]
        
        # Categorized food items
        self.food_categories = {
            "meat": ["chicken", "beef", "pork", "lamb", "turkey", "duck", "goat", "sausage", "bacon", "veal"],
            "fish_and_seafood": ["salmon", "tuna", "shrimp", "crab", "lobster", "cod", "trout", "mackerel", "octopus", "squid"],
            "vegetables": ["carrot", "broccoli", "spinach", "kale", "lettuce", "potato", "onion", "tomato", "cucumber", "zucchini", "pepper", "asparagus", "eggplant", "garlic", "sweet potato", "mushrooms"],
            "fruits": ["apple", "banana", "orange", "grape", "strawberry", "blueberry", "kiwi", "pineapple", "mango", "pear", "watermelon", "peach", "plum", "cherry", "pomegranate", "cantaloupe"],
            "grains": ["rice", "quinoa", "wheat", "barley", "oats", "corn", "millet", "farro", "couscous", "bulgur", "sorghum"],
            "dairy": ["milk", "cheese", "yogurt", "butter", "cream", "cream cheese", "sour cream", "cottage cheese", "mozzarella", "parmesan", "feta", "ricotta"],
            "nuts": ["almond", "walnut", "cashew", "pecan", "hazelnut", "macadamia", "brazil nut", "pistachio", "pine nut", "filberts"],
            "seeds": ["chia seeds", "flaxseeds", "sunflower seeds", "pumpkin seeds", "sesame seeds", "hemp seeds", "poppy seeds"],
            "legumes": ["lentils", "chickpeas", "black beans", "kidney beans", "pinto beans", "navy beans", "green beans", "peas", "soybeans", "edamame"],
            "herbs_and_spices": ["basil", "parsley", "cilantro", "thyme", "oregano", "rosemary", "sage", "tarragon", "dill", "mint", "cumin", "turmeric", "paprika", "black pepper", "cardamom", "coriander", "clove", "bay leaf", "nutmeg", "cinnamon", "ginger", "garlic powder"],
            "beverages": ["coffee", "tea", "water", "juice", "soda", "beer", "wine", "smoothie", "milkshake", "cocktail", "energy drink"],
            "snacks": ["chips", "popcorn", "pretzels", "crackers", "nachos", "cheese sticks", "granola bars", "trail mix", "cookies", "candy", "chocolate", "gummy bears", "granola", "fruit roll-up"],
            "sweets": ["cake", "cookie", "pie", "brownie", "donut", "muffin", "cupcake", "ice cream", "chocolate", "pudding", "candy", "fudge", "tart", "macaron", "cheesecake", "jelly", "marzipan"],
            "sauces_and_condiments": ["ketchup", "mustard", "mayonnaise", "barbecue sauce", "hot sauce", "soy sauce", "sriracha", "vinaigrette", "salsa", "hummus", "tahini", "ranch dressing", "blue cheese dressing", "teriyaki sauce", "mayo", "horseradish"],
            "breads_and_bakery": ["bread", "bagel", "croissant", "roll", "ciabatta", "sourdough", "tortilla", "pita", "naan", "brioche", "muffin", "focaccia"],
            "fast_food": ["pizza", "burger", "fries", "hot dog", "chicken nuggets", "sandwich", "wrap", "taco", "sushi", "fried chicken", "gyros", "spring roll", "shawarma", "falafel"],
            "pasta_and_noodles": ["spaghetti", "penne", "macaroni", "fettuccine", "ravioli", "lasagna", "noodles", "udon", "ramen", "soba", "gnocchi"],
            "pizza_toppings": ["pepperoni", "mushrooms", "sausage", "onions", "green peppers", "tomato", "olives", "cheese", "pineapple", "ham", "bacon", "spinach", "artichoke"],
            "miscellaneous_foods": ["tofu", "seitan", "tempeh", "veggie burger", "miso", "avocado", "coconut", "rice cake", "seaweed", "kimchi", "pickles"]
        }

    def classify_intent(self, user_input):
        """
        Classifies the user's input based on predefined intents.
        """
        user_input_lower = user_input.lower()
        print(user_input_lower)

        # Check for matching intents based on keywords
        matched_intents = [
            intent for intent, keywords in self.intents.items() if any(keyword in user_input_lower for keyword in keywords)
        ]
        
        # Return intent based on matching categories
        if "request_recipe" in matched_intents:
            return "request_recipe"
        elif "greet" in matched_intents:
            return "greet"
        elif "specify_allergies" in matched_intents:
            return "specify_allergies"
        elif "search_information" in matched_intents:
            return "search_information"

        return "unknown"

    def extract_information(self, user_input):
        """
        Extracts food-related information such as ingredients, allergies, and diet preferences.
        """
        doc = self.nlp(user_input)
        ingredients = []
        allergies = []
        diet = None

        # Create a mapping of food keywords to their categories
        food_keywords = {food: category for category, foods in self.food_categories.items() for food in foods}

        for token in doc:
            token_text = token.text.lower()

            # Extract diet-related information
            if token_text in self.diet_keywords:
                diet = token_text

            # Extract allergy-related information
            if token_text in self.allergy_keywords:
                # Check for food-related terms before/after the allergy-related term
                if token.i > 0 and doc[token.i - 1].text.lower() in food_keywords:
                    allergies.append(doc[token.i - 1].text)
                if token.i < len(doc) - 1 and doc[token.i + 1].text.lower() in food_keywords:
                    allergies.append(doc[token.i + 1].text)
                if token.i < len(doc) - 2 and doc[token.i + 1].pos_ == "ADP" and doc[token.i + 2].text.lower() in food_keywords:
                    allergies.append(doc[token.i + 2].text)

            # Extract ingredients from food categories
            elif token.pos_ == "NOUN" and token_text in food_keywords:
                ingredients.append((token.text, food_keywords[token_text]))

        return ingredients, allergies, diet