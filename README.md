# Project Plan

## Research Question
**How can enhancing a chatbot with multi-modal interactions improve its ability to provide personalized recipe suggestions and answer FAQs effectively?**

## Project Overview
To investigate the impact of multi-modal interactions on chatbot effectiveness, we will develop a web-based prototype that integrates the chatbot. The website will feature a user-friendly interface where users can interact with the chatbot via text.

### Key Features:
- **Natural Language Processing (NLP):** We will use existing NLP libraries for intent recognition to help the chatbot understand user requests.
- **Multi-modal interactions:** This will enhance the chatbot’s ability to provide personalized recipe suggestions and answer FAQs.
- **Website Interface:** A web-based interface will allow users to interact with the chatbot directly.

We will conduct a literature review on chatbot design and user engagement to guide the development and implementation. Through iterative testing and user feedback, we will refine the chatbot’s capabilities.

### Technologies:
- **Rasa Framework:** Leverage its NLP capabilities for intent recognition and dialogue management.
- **Frontend:** HTML, CSS, JavaScript (React, Bootstrap for dynamic components).
- **Backend:** Flask/Django to set up a server that handles API requests and communicates with the Rasa chatbot.

---

## Current Progress
- **Resource Pool:** A collection of tutorials, blog posts, and datasets has been gathered to help build the chatbot.
- **Recipe Data:** Databases and APIs are selected for recipe retrieval and Q&A purposes.

### Resources:
- **Recipe Search Algorithms:**
  - [Fuzzy Matching in Python](https://pypi.org/project/fuzzywuzzy/) – A Python package for matching words based on similarity, useful for ingredient lookups.
  
- **Recipe Databases & APIs:**
  - [Epicurious Dataset](https://www.kaggle.com/datasets/hugodarwood/epirecipes)
  - [Kaggle Dataset with Recipes by Rating and Nutrition](https://spoonacular.com/food-api)
  - [Edam API](https://www.edamam.com/)
  - [TheMealDB API](https://www.themealdb.com/api.php)
  - **Spoonacular API**
    - Description: Offers a wide range of features including searching recipes, meal plans, ingredient lists, and nutritional information.
    - Pricing: Limited to 150 requests per day.
    - Features: Search recipes by ingredients, get recipe instructions, images, and more. Provides data on nutrition, diet, and meal plans.
  
  - **Edamam API**
    - Description: Provides access to a large database of recipes and nutrition information.
    - Pricing: Limited number of API calls per month.
    - Features: Search for recipes by ingredients, dietary preferences, cuisine, and more. Analyze the nutritional content of recipes and individual ingredients.
  
  - **TheMealDB API**
    - Description: A free, open-source API for recipes, allowing users to search recipes by name, ingredient, and category.
    - Pricing: Free access without restrictions (community-supported).
    - Features: Search recipes by ingredients, name, or cuisine. Get recipe images, instructions, and ingredient lists.

### Tutorials:
- **Machine Learning for Recipe Recommendation:** [Recommendation System Algorithms in Python (Kaggle)](https://www.kaggle.com/code/prashant111/recommender-systems-in-python)
  - A guide to implementing recommendation systems using collaborative filtering or content-based approaches.
- **Frontend Integration for Bot UI:** Flask Web Framework

---

## Project Timeline
### Phase 2: Research & Data Collection
- **Task:** Read research articles on chatbots, NLP, and recipe recommendations.
- **Task:** Gather resources on multi-modal interactions.
- **Task:** Clean and organize data.

### Phase 3: Learning & Design
- **Phase 3.1: Learning**
  - Learn Rasa framework and its features.
  - Familiarize with Flask/Django and front-end technologies (HTML/CSS/JS).
  
- **Phase 3.2: Initial Design and Planning**
  - Define user personas and chatbot flows.
  - Sketch the web interface.

### Phase 4: Development
- **Task:** Develop the chatbot using Rasa.
- **Task:** Implement the front-end interface.
- **Task:** Set up the backend with Flask/Django.
- **Task:** Write a project paper detailing progress.

### Phase 5: Integration & Testing
- **Phase 5.1: Integration**
  - Integrate the chatbot with the web interface.
  - Connect the database for storing user data and recipes.
  
- **Phase 5.2: Testing and Analysis**
  - Conduct user testing to gather feedback, analyze performance, and make adjustments.

- **Phase 5.3: Final Presentation**
  - Compile documentation and prepare for the presentation.
  - Create a poster showcasing user guides and chatbot features.
