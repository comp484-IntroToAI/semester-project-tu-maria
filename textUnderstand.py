import spacy

class TextUnderstanding:
    def __init__(self):
        # Load small English model from spaCy
        self.nlp = spacy.load("en_core_web_sm")
        
        # Intent dictionary for classification
        self.intents = {
            "greet": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
            "request_recipe": ["recipe", "cook", "make", "prepare", "dish", "meal"],
            "specify_allergies": ["allergy", "allergies", "allergic", "without", "no", "free", "intolerance", "sensitive", "avoid"],
            "search_information": ["ingredient", "nutrition", "calories", "fat", "protein", "carbohydrates", "vitamins"],
        }
        
        # Diet-related keywords
        self.diet_keywords = ["gluten free", "ketogenic", "vegetarian", "lacto-vegetarian", "ovo-vegetarian", "vegan", "pescetarian", "paleo", "primal", "low fodmap", "whole30"]
        
        # Allergy-related keywords
        self.allergy_keywords = ["allergy", "allergic", "without", "no", "free", "intolerance", "sensitive", "avoid"]
        
        # Food categories and their respective keywords
        self.food_categories = {
            # Meat and Poultry
            "meat": ["chicken", "beef", "pork", "lamb", "turkey", "duck", "goat", "sausage", "bacon", "veal"],
            
            # Fish and Seafood
            "fish_and_seafood": ["salmon", "tuna", "shrimp", "crab", "lobster", "cod", "trout", "mackerel", "octopus", "squid"],
            
            # Vegetables
            "vegetables": ["carrot", "broccoli", "spinach", "kale", "lettuce", "potato", "onion", "tomato", "cucumber", "zucchini", "pepper", "asparagus", "eggplant", "garlic", "sweet potato", "mushrooms"],
            
            # Fruits
            "fruits": ["apple", "banana", "orange", "grape", "strawberry", "blueberry", "kiwi", "pineapple", "mango", "pear", "watermelon", "peach", "plum", "cherry", "pomegranate", "cantaloupe"],
            
            # Grains and Cereals
            "grains": ["rice", "quinoa", "wheat", "barley", "oats", "corn", "millet", "farro", "couscous", "bulgur", "sorghum"],
            
            # Dairy
            "dairy": ["milk", "cheese", "yogurt", "butter", "cream", "cream cheese", "sour cream", "cottage cheese", "mozzarella", "parmesan", "feta", "ricotta"],
            
            # Nuts and Seeds
            "nuts": ["almond", "walnut", "cashew", "pecan", "hazelnut", "macadamia", "brazil nut", "pistachio", "pine nut", "filberts"],
            "seeds": ["chia seeds", "flaxseeds", "sunflower seeds", "pumpkin seeds", "sesame seeds", "hemp seeds", "poppy seeds"],
            
            # Legumes
            "legumes": ["lentils", "chickpeas", "black beans", "kidney beans", "pinto beans", "navy beans", "green beans", "peas", "soybeans", "edamame"],
            
            # Herbs and Spices
            "herbs_and_spices": ["basil", "parsley", "cilantro", "thyme", "oregano", "rosemary", "sage", "tarragon", "dill", "mint", "cumin", "turmeric", "paprika", "black pepper", "cardamom", "coriander", "clove", "bay leaf", "nutmeg", "cinnamon", "ginger", "garlic powder"],
            
            # Beverages
            "beverages": ["coffee", "tea", "water", "juice", "soda", "beer", "wine", "smoothie", "milkshake", "cocktail", "energy drink"],
            
            # Snacks
            "snacks": ["chips", "popcorn", "pretzels", "crackers", "nachos", "cheese sticks", "granola bars", "trail mix", "cookies", "candy", "chocolate", "gummy bears", "granola", "fruit roll-up"],
            
            # Sweets
            "sweets": ["cake", "cookie", "pie", "brownie", "donut", "muffin", "cupcake", "ice cream", "chocolate", "pudding", "candy", "fudge", "tart", "macaron", "cheesecake", "jelly", "marzipan"],
            
            # Sauces and Condiments
            "sauces_and_condiments": ["ketchup", "mustard", "mayonnaise", "barbecue sauce", "hot sauce", "soy sauce", "sriracha", "vinaigrette", "salsa", "hummus", "tahini", "ranch dressing", "blue cheese dressing", "teriyaki sauce", "mayo", "horseradish"],
            
            # Breads and Bakery Items
            "breads_and_bakery": ["bread", "bagel", "croissant", "roll", "ciabatta", "sourdough", "tortilla", "pita", "naan", "brioche", "muffin", "focaccia"],
            
            # Fast Food and Convenience Foods
            "fast_food": ["pizza", "burger", "fries", "hot dog", "chicken nuggets", "sandwich", "wrap", "taco", "sushi", "fried chicken", "gyros", "spring roll", "shawarma", "falafel"],
            
            # Pasta and Noodles
            "pasta_and_noodles": ["spaghetti", "penne", "macaroni", "fettuccine", "ravioli", "lasagna", "noodles", "udon", "ramen", "soba", "gnocchi"],
            
            # Pizza Toppings
            "pizza_toppings": ["pepperoni", "mushrooms", "sausage", "onions", "green peppers", "tomato", "olives", "cheese", "pineapple", "ham", "bacon", "spinach", "artichoke"],
            
            # Miscellaneous Foods
            "miscellaneous_foods": ["tofu", "seitan", "tempeh", "veggie burger", "miso", "avocado", "coconut", "rice cake", "seaweed", "kimchi", "pickles"]
        }

        
    def classify_intent(self, user_input):
        """
        Classifies the user's input based on predefined intents.
        """
        user_input_lower = user_input.lower()
        print(user_input_lower)  # Debugging output
        matched_intents = []

        for intent, keywords in self.intents.items():
            if any(keyword in user_input_lower for keyword in keywords):
                matched_intents.append(intent)

        # Prioritize specific intents over general ones
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
        
        # Create a mapping of all foods to their categories for easy lookup
        food_keywords = {food: category for category, foods in self.food_categories.items() for food in foods}
        food_categories = set(self.food_categories.keys())

        for token in doc:
            # Check for diet-related keywords
            if token.text.lower() in self.diet_keywords:
                diet = token.text
            
            # Check for allergy-related keywords and extract nearby food items
            elif token.text.lower() in self.allergy_keywords:
                # Check adjacent tokens for food mentions
                if token.i > 0 and doc[token.i - 1].text.lower() in food_keywords:
                    allergies.append(doc[token.i - 1].text)
                if token.i < len(doc) - 1 and doc[token.i + 1].text.lower() in food_keywords:
                    allergies.append(doc[token.i + 1].text)
                if token.i < len(doc) - 2 and doc[token.i + 1].pos_ == "ADP" and doc[token.i + 2].text.lower() in food_keywords:
                    allergies.append(doc[token.i + 2].text)
            
            # Check for food ingredients
            elif token.pos_ == "NOUN" and token.text.lower() in food_keywords:
                ingredients.append((token.text, food_keywords[token.text.lower()]))

        # Return extracted information
        return ingredients, allergies, diet