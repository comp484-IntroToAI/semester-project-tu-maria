import spacy

class TextUnderstanding:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.intents = {
            "greet": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
            "request_recipe": ["recipe", "cook", "make", "prepare", "dish", "meal"],
            "specify_allergies": ["allergy", "allergies", "allergic", "without", "no", "free", "intolerance", "sensitive", "avoid"],
            "search_information": ["ingredient", "nutrition", "calories", "fat", "protein", "carbohydrates", "vitamins"],
        }
        self.diet_keywords = ["vegan", "vegetarian", "keto", "paleo", "low-carb", "gluten-free", "dairy-free", "nut-free", "soy-free", "sugar-free", "low-fat", "high-protein", "Mediterranean", "intermittent fasting", "raw", "low-sodium", "clean eating", "diabetic", "weight watchers"]
        self.allergy_keywords = ["allergy", "allergic", "without", "no", "free", "intolerance", "sensitive", "avoid"]
        self.food_categories = {
            "meat": ["chicken", "beef", "pork", "lamb", "turkey"],
            "fish_and_seafood": ["salmon", "tuna", "shrimp", "crab", "lobster"],
            "vegetables": ["carrot", "broccoli", "spinach", "kale", "lettuce"],
            "fruits": ["apple", "banana", "orange", "grape", "strawberry"],
            "grains": ["rice", "quinoa", "wheat", "barley", "oats"],
            "dairy": ["milk", "cheese", "yogurt", "butter", "cream"],
            "nuts": ["almond", "walnut", "cashew", "pecan", "hazelnut"],
            "seeds": ["chia seeds", "flaxseeds", "sunflower seeds", "pumpkin seeds"],
            "legumes": ["lentils", "chickpeas", "black beans", "kidney beans"],
            "herbs_and_spices": ["basil", "parsley", "cilantro", "thyme", "oregano"]
        }

    def classify_intent(self, user_input):
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
        doc = self.nlp(user_input)
        ingredients = []
        allergies = []
        diet = None
        
        food_keywords = {food: category for category, foods in self.food_categories.items() for food in foods}
        food_categories = set(self.food_categories.keys())

        for token in doc:
            if token.text.lower() in self.diet_keywords:
                diet = token.text
            elif token.text.lower() in self.allergy_keywords:
                if token.i > 0:
                    if doc[token.i - 1].text.lower() in food_keywords or doc[token.i - 1].text.lower() in food_categories:
                        allergies.append(doc[token.i - 1].text)
                        break
                if token.i < len(doc) - 1:
                    if doc[token.i + 1].text.lower() in food_keywords or doc[token.i + 1].text.lower() in food_categories:
                        allergies.append(doc[token.i + 1].text)
                        break
                if token.i < len(doc) - 2 and doc[token.i + 1].pos_ == "ADP":
                    if doc[token.i + 2].text.lower() in food_keywords or doc[token.i + 2].text.lower() in food_categories:
                        allergies.append(doc[token.i + 2].text)
                        break
            elif token.pos_ == "NOUN" and token.text.lower() in food_keywords:
                ingredients.append((token.text, food_keywords[token.text.lower()]))

        return ingredients, allergies, diet