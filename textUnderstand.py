import spacy

class TextUnderstanding:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Define the intents with associated keywords
        self.intents = {
            "greet": ["good afternoon", "good evening", "good morning", "hello", "hey", "hi"],
            "specify_allergies": ["allergy", "allergies", "avoid", "intolerance", "no", "sensitive", "without", "free", "no"],
            "search_information": [
                "calories", "carbohydrates", "cholesterol", "content", "energy", "fact", "fiber", "ingredient", "ingredients", 
                "information", "macro", "micronutrients", "minerals", "nutrition", "nutrients", "nutritional", "protein", 
                "sodium", "sugars", "value", "vitamin", "vitamins"
            ],
            "request_recipe": ["cook", "dish", "make", "meal", "prepare", "recipe"],
            "specify_diet": [
                "anti-cancer", "anti-inflammatory", "autoimmune-protocol", "diabetic-friendly", "dairy-free", "fasting", 
                "flexitarian", "gluten-free", "grain-free", "heart-healthy", "high-fat", "high-protein", "intermittent-fasting", 
                "keto", "ketogenic", "low-calorie", "low-cholesterol", "low-fat", "low-carb", "low-glycemic", "low-sodium", 
                "low-sugar", "lacto-vegetarian", "Mediterranean", "no-carb", "no-dairy", "no-gluten", "no-meat", "nut-free", 
                "paleo", "plant-based", "plant-forward", "pescetarian", "primal", "raw", "sugar-free", "soy-free", "vegetarian", 
                "vegan", "whole-food", "whole30"
            ]
        }

        
        # Diet-related keywords
        self.diet_keywords = [
            "anti-cancer", "anti-inflammatory", "autoimmune-protocol", "diabetic-friendly", "dairy-free", "fasting", 
            "flexitarian", "gluten-free", "grain-free", "heart-healthy", "high-fat", "high-protein", "intermittent-fasting", 
            "keto", "ketogenic", "low-calorie", "low-cholesterol", "low-fat", "low-carb", "low-glycemic", "low-sodium", 
            "low-sugar", "lacto-vegetarian", "Mediterranean", "no-carb", "no-dairy", "no-gluten", "no-meat", "nut-free", 
            "paleo", "plant-based", "plant-forward", "pescetarian", "primal", "raw", "sugar-free", "soy-free", "vegetarian", 
            "vegan", "whole-food", "whole30"
        ]
        
        # Allergy-related keywords
        self.allergy_keywords = ["allergy", "allergic", "without", "no", "free", "intolerance", "sensitive", "avoid"]
        
        # Categorized food items
        self.food_categories = {
            "meat": ["chicken", "beef", "pork", "lamb", "turkey", "duck", "goat", "sausage", "bacon", "veal", "steak", "ribeye", "brisket", "ground beef", "chorizo", "bison", "kangaroo", "pâté", "salami", "prosciutto"],
            "fish_and_seafood": ["salmon", "tuna", "shrimp", "crab", "lobster", "cod", "trout", "mackerel", "octopus", "squid", "tilapia", "sardine", "herring", "snapper", "halibut", "clams", "mussels", "scallops", "sea bass", "swordfish", "anchovies"],
            "vegetables": ["carrot", "broccoli", "spinach", "kale", "lettuce", "potato", "onion", "tomato", "cucumber", "zucchini", "pepper", "asparagus", "eggplant", "garlic", "sweet potato", "mushrooms", "artichoke", "beetroot", "radish", "brussels sprouts", "cauliflower", "celery", "pumpkin", "butternut squash"],
            "fruits": ["apple", "banana", "orange", "grape", "strawberry", "blueberry", "kiwi", "pineapple", "mango", "pear", "watermelon", "peach", "plum", "cherry", "pomegranate", "cantaloupe", "apricot", "nectarine", "fig", "papaya", "blackberry", "raspberry", "lychee", "coconut", "dragon fruit", "persimmon", "tangerine"],
            "grains": ["rice", "quinoa", "wheat", "barley", "oats", "corn", "millet", "farro", "couscous", "bulgur", "sorghum", "buckwheat", "spelt", "teff", "amaranth", "wild rice", "polenta", "polenta", "rye", "freekeh", "black rice", "brown rice", "white rice"],
            "dairy": ["milk", "cheese", "yogurt", "butter", "cream", "cream cheese", "sour cream", "cottage cheese", "mozzarella", "parmesan", "feta", "ricotta", "gouda", "brie", "cheddar", "blue cheese", "camembert", "swiss cheese", "cream cheese", "mascarpone", "goat cheese", "grana padano", "ricotta salata", "havarti", "provolone"],
            "nuts": ["almond", "walnut", "cashew", "pecan", "hazelnut", "macadamia", "brazil nut", "pistachio", "pine nut", "filberts", "chestnut", "marcona almonds", "cashew butter", "peanut", "peanut butter", "almond butter", "sunflower seeds", "pumpkin seeds", "walnut butter", "nutmeg"],
            "seeds": ["chia seeds", "flaxseeds", "sunflower seeds", "pumpkin seeds", "sesame seeds", "hemp seeds", "poppy seeds", "cumin seeds", "caraway seeds", "mustard seeds", "fenugreek seeds", "melon seeds", "watermelon seeds", "quinoa seeds", "sunflower kernel", "chia seed powder"],
            "legumes": ["lentils", "chickpeas", "black beans", "kidney beans", "pinto beans", "navy beans", "green beans", "peas", "soybeans", "edamame", "mung beans", "split peas", "black-eyed peas", "fava beans", "garbanzo beans", "peanut", "lupini beans", "aduki beans", "cranberry beans", "butter beans", "kidney beans"],
            "herbs_and_spices": ["basil", "parsley", "cilantro", "thyme", "oregano", "rosemary", "sage", "tarragon", "dill", "mint", "cumin", "turmeric", "paprika", "black pepper", "cardamom", "coriander", "clove", "bay leaf", "nutmeg", "cinnamon", "ginger", "garlic powder", "chili powder", "fennel seeds", "allspice", "garam masala", "cayenne pepper", "mustard", "saffron"],
            "beverages": ["coffee", "tea", "water", "juice", "soda", "beer", "wine", "smoothie", "milkshake", "cocktail", "energy drink", "latte", "espresso", "cappuccino", "green tea", "black tea", "herbal tea", "lemonade", "fruit punch", "iced tea", "kombucha", "ginger ale", "sparkling water", "hot chocolate", "milk", "wine spritzer", "sangria"],
            "snacks": ["chips", "popcorn", "pretzels", "crackers", "nachos", "cheese sticks", "granola bars", "trail mix", "cookies", "candy", "chocolate", "gummy bears", "granola", "fruit roll-up", "beef jerky", "rice cakes", "vegetable crisps", "fruit chips", "cheese puffs", "protein bars", "dark chocolate", "fruit leather", "baked chips", "rice crackers"],
            "sweets": ["cake", "cookie", "pie", "brownie", "donut", "muffin", "cupcake", "ice cream", "chocolate", "pudding", "candy", "fudge", "tart", "macaron", "cheesecake", "jelly", "marzipan", "churros", "panna cotta", "tiramisu", "baklava", "caramel", "eclair", "flan", "profiteroles", "nougat", "truffles", "cookies and cream", "mochi"],
            "sauces_and_condiments": ["ketchup", "mustard", "mayonnaise", "barbecue sauce", "hot sauce", "soy sauce", "sriracha", "vinaigrette", "salsa", "hummus", "tahini", "ranch dressing", "blue cheese dressing", "teriyaki sauce", "mayo", "horseradish", "pesto", "chimichurri", "tartar sauce", "mole", "aioli", "chili sauce", "buffalo sauce", "hoisin sauce", "lemon curd", "Worcestershire sauce"],
            "breads_and_bakery": ["bread", "bagel", "croissant", "roll", "ciabatta", "sourdough", "tortilla", "pita", "naan", "brioche", "muffin", "focaccia", "croissant", "ciabatta", "pumpernickel", "scone", "breadsticks", "brioche", "baguette", "whole wheat bread", "flatbread", "english muffin", "rye bread", "zucchini bread", "banana bread", "garlic bread"],
            "fast_food": ["pizza", "burger", "fries", "hot dog", "chicken nuggets", "sandwich", "wrap", "taco", "sushi", "fried chicken", "gyros", "spring roll", "shawarma", "falafel", "fish and chips", "chicken sandwich", "buffalo wings", "quesadilla", "chili cheese fries", "poutine", "pork belly bun", "corn dog", "pasta salad", "french toast", "mozzarella sticks"],
            "pasta_and_noodles": ["spaghetti", "penne", "macaroni", "fettuccine", "ravioli", "lasagna", "noodles", "udon", "ramen", "soba", "gnocchi", "fusilli", "orzo", "linguine", "pappardelle", "farfalle", "cavatappi", "tagliatelle", "capellini", "tortellini", "ziti", "manicotti", "stuffed shells", "rigatoni", "pesto pasta", "carbonara", "alfredo", "bolognese"],
            "pizza_toppings": ["pepperoni", "mushrooms", "sausage", "onions", "green peppers", "tomato", "olives", "cheese", "pineapple", "ham", "bacon", "spinach", "artichoke", "anchovies", "jalapeños", "chicken", "ground beef", "feta", "eggplant", "sun-dried tomatoes", "cheddar", "salami", "ricotta", "parmesan", "goat cheese", "broccoli", "salami"],
            "miscellaneous_foods": ["tofu", "seitan", "tempeh", "veggie burger", "miso", "avocado", "coconut", "rice cake", "seaweed", "kimchi", "pickles", "jackfruit", "marmite", "nut butter", "soy milk", "almond milk", "coconut milk", "pita chips", "hummus", "coconut yogurt", "sauerkraut", "nutritional yeast", "plant-based cheese", "rice noodles", "fermented foods", "pea protein", "chia pudding"]
        }

    def classify_intent(self, user_input):
        """
        Classifies the user's input based on predefined intents.
        """
        user_input_lower = user_input.lower()

        # Check for matching intents based on keywords
        matched_intents = [
            intent for intent, keywords in self.intents.items() if any(keyword in user_input_lower for keyword in keywords)
        ]
        
        # If food-related keywords are found in user input, classify as a request for a recipe
        food_items_in_input = [
            food for food_list in self.food_categories.values() for food in food_list if food in user_input_lower
        ]
        
        if food_items_in_input:
            return "request_recipe"

        # If diet-related keywords are found, classify as specify_diet
        diet_items_in_input = [keyword for keyword in self.diet_keywords if keyword in user_input_lower]
        if diet_items_in_input:
            return "specify_diet"

        # Return the first matching intent based on predefined categories
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