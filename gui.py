import tkinter as tk
from tkinter import scrolledtext

from recommendRecipe import RecipeRecommender
from textUnderstand import TextUnderstanding

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("RecipeGenie")
        self.master.configure(bg='#caf0f8')

        self.text_understanding = TextUnderstanding()
        self.recommender = RecipeRecommender()

        # Create clear button with colored border
        self.clear_button = tk.Button(
            master,
            text="Clear",
            command=self.clear_chat,
            highlightbackground='#caf0f8',
            highlightcolor='#ade8f4',
            highlightthickness=2
        )
        self.clear_button.grid(column=0, row=0, padx=10, pady=(10, 0), sticky='nw')

        # Create chat area with colored border
        self.chat_display = scrolledtext.ScrolledText(
            master,
            wrap=tk.WORD,
            state='disabled',
            bg='white',
            fg='black',
            highlightbackground='#caf0f8',
            highlightcolor='#ade8f4',
            highlightthickness=2
        )
        self.chat_display.grid(column=0, row=1, padx=10, pady=10, sticky='nsew')

        # Create user input area with colored border
        self.user_input = tk.Entry(
            master,
            bg='white',
            fg='black',
            highlightbackground='#caf0f8',
            highlightcolor='#ade8f4',
            highlightthickness=2
        )
        self.user_input.grid(column=0, row=2, padx=10, pady=(0, 10), sticky='ew')

        self.placeholder = "Please specify your recipe preferences."
        self.user_input.insert(0, self.placeholder)
        self.user_input.configure(fg='lightgrey')
        
        self.user_input.bind("<FocusIn>", self.on_entry_click)
        self.user_input.bind("<FocusOut>", self.on_focusout)
        self.user_input.bind('<Return>', lambda event: self.send_message())

        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)

    def on_entry_click(self, event):
        if self.user_input.get() == self.placeholder:
            self.user_input.delete(0, tk.END)
            self.user_input.configure(fg='black')

    def on_focusout(self, event):
        if self.user_input.get() == '':
            self.user_input.insert(0, self.placeholder)
            self.user_input.configure(fg='lightgrey')

    def send_message(self):
        user_input = self.user_input.get()
        if user_input == self.placeholder or user_input.strip() == '':
            return

        self._add_message(user_input, "user")
        intent = self.text_understanding.classify_intent(user_input)
        ingredients, allergies, diet = self.text_understanding.extract_information(user_input)

        # Convert ingredients from list of tuples to just the ingredient names
        ingredient_names = [ingredient[0] for ingredient in ingredients]

        response = self.generate_response(intent, ingredient_names, allergies, diet)
        self._add_message(response, "bot")

        self.chat_display.yview(tk.END)
        self.user_input.delete(0, tk.END)

    def _add_message(self, message, sender):
        self.chat_display.configure(state='normal')

        spacing = "\n"
        
        if sender == "user":
            self.chat_display.insert(tk.END, spacing + message + "\n", "user")
            self.chat_display.tag_config("user", justify='right')
        else:
            # Break message into lines based on chatbox width
            wrapped_message = self.wrap_message(message)
            self.chat_display.insert(tk.END, spacing + wrapped_message + "\n", "bot")
            self.chat_display.tag_config("bot", justify='left')

        self.chat_display.configure(state='disabled')

    def clear_chat(self):
        self.chat_display.configure(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state='disabled')

    def wrap_message(self, message):
        """Wrap the message to 80% of the chatbox width."""
        # Estimate the width of a character in the current font
        char_width = 7

        # Get the width of the chat box (in pixels)
        chat_width = self.chat_display.winfo_width()

        # Set the desired width to 80% of the chatbox width
        max_line_length = int(chat_width * 0.9 // char_width)

        # Split the message into chunks that fit within the max line length
        lines = []
        while len(message) > max_line_length:
            # Find the last space within the limit to split at
            split_point = message.rfind(' ', 0, max_line_length)
            if split_point == -1:
                split_point = max_line_length
            lines.append(message[:split_point])
            message = message[split_point:].lstrip()

        # Add the remaining message
        if message:
            lines.append(message)

        return "\n".join(lines)

    def generate_response(self, intent, ingredients, allergies, diet):
        if intent == "greet":
            return "Hi! How can I help you?"
        elif intent == "request_recipe":
            # Print and process the recipe request
            print(f"ingredients: {ingredients}")
            print(f"allergies: {allergies}")
            print(f"diet: {diet}")

            # Set user profile with exclusions and diet
            self.recommender.user_profile["excluded_ingredients"] = allergies
            self.recommender.user_profile["diet"] = diet

            # Search for recipes
            recipes = self.recommender.search_recipes(ingredients)

            if recipes:
                first_recipe_details = self.recommender.fetch_recipe_details(recipes[0]['id'])
                self.recommender.display_recipe(first_recipe_details)

                # Show recipe details in the GUI (instead of console)
                recipe_info = f"Recipe: {first_recipe_details[0]}\n"
                recipe_info += f"Image: {first_recipe_details[1]}\n"
                recipe_info += f"Ingredients: {', '.join(first_recipe_details[2])}\n"
                recipe_info += f"Instructions: {first_recipe_details[3]}\n"

                return recipe_info

            else:
                return "Sorry, no recipes found with the given ingredients."
        elif intent == "specify_allergies":
            return "Please specify your allergies to avoid those ingredients."
        elif intent == "search_information":
            return "Searching for information..."
        else:
            return "I'm not sure how to help with that."

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = ChatbotGUI(root)
    root.mainloop()
