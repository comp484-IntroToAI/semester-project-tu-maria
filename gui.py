import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import requests
from PIL import Image, ImageTk
from io import BytesIO

from recommendRecipe import RecipeRecommender
from textUnderstand import TextUnderstanding

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ChefBot")
        self.master.configure(bg='#caf0f8')

        # Initialize components
        self.text_understanding = TextUnderstanding()
        self.recommender = RecipeRecommender()

        self.speech_recognition_active = False
        self.placeholder = "Please specify your recipe preferences."
        self.voice_input = False

        self.tts_engine = pyttsx3.init()

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        """Create and layout the widgets on the window."""
        self.create_clear_button()
        self.create_chat_display()
        self.create_input_frame()
        self.create_user_input()
        self.create_speak_button()

        # Configure grid weights
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)

    def create_clear_button(self):
        """Create the 'Clear' button."""
        self.clear_button = tk.Button(
            self.master,
            text="Clear",
            command=self.clear_chat,
            highlightbackground='#caf0f8',
            highlightcolor='#ade8f4',
            highlightthickness=2
        )
        self.clear_button.grid(column=0, row=0, padx=10, pady=(10, 0), sticky='nw')

    def create_chat_display(self):
        """Create the chat display area."""
        self.chat_display = scrolledtext.ScrolledText(
            self.master,
            wrap=tk.WORD,
            state='disabled',
            bg='white',
            fg='black',
            highlightbackground='#caf0f8',
            highlightcolor='#ade8f4',
            highlightthickness=2
        )
        self.chat_display.grid(column=0, row=1, padx=10, pady=10, sticky='nsew')

    def create_input_frame(self):
        """Create the frame containing the user input and voice button."""
        self.input_frame = tk.Frame(self.master, bg='#caf0f8')
        self.input_frame.grid(column=0, row=2, padx=10, pady=(0, 10), sticky='ew')

    def create_user_input(self):
        """Create the user input field."""
        self.user_input = tk.Entry(
            self.input_frame,
            bg='white',
            fg='black',
            highlightbackground='#caf0f8',
            highlightcolor='#ade8f4',
            highlightthickness=2
        )
        self.user_input.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Placeholder text
        self.user_input.insert(0, self.placeholder)
        self.user_input.configure(fg='lightgrey')

        # Bind events
        self.user_input.bind("<FocusIn>", self.on_entry_click)
        self.user_input.bind("<FocusOut>", self.on_focusout)
        self.user_input.bind('<Return>', lambda event: self.send_message())

    def create_speak_button(self):
        """Create the 'Voice' button for speech recognition."""
        self.speak_button = tk.Button(
            self.input_frame,
            text="Voice",
            command=self.start_speech_recognition,
            highlightbackground='#caf0f8',
            highlightcolor='#ade8f4',
            highlightthickness=2
        )
        self.speak_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    # ----- User Input Handling -----
    def on_entry_click(self, event):
        """Handles focus in event for the input field."""
        if self.user_input.get() == self.placeholder:
            self.user_input.delete(0, tk.END)
            self.user_input.configure(fg='black')

    def on_focusout(self, event):
        """Handles focus out event for the input field."""
        if not self.user_input.get():
            self.user_input.insert(0, self.placeholder)
            self.user_input.configure(fg='lightgrey')

    def send_message(self):
        """Process the user input and generate a bot response."""
        user_input = self.user_input.get().strip()

        if user_input == self.placeholder or not user_input:
            return

        if not self.speech_recognition_active:
            self._add_message(user_input, "user")

        # Classify the intent and extract relevant info
        intent = self.text_understanding.classify_intent(user_input)
        ingredients, allergies, diet = self.text_understanding.extract_information(user_input)

        ingredient_names = [ingredient[0] for ingredient in ingredients]
        response = self.generate_response(intent, ingredient_names, allergies, diet)

        self._add_message(response, "bot")
        self.chat_display.yview(tk.END)

        self.user_input.delete(0, tk.END)

        # If voice input, convert response to speech
        if self.voice_input:
            self.text_to_speech(response)

    def _add_message(self, message, sender):
        """Add a message to the chat display."""
        self.chat_display.configure(state='normal')
        
        spacing = "\n"
        if sender == "user":
            self.chat_display.insert(tk.END, spacing + message + "\n", "user")
            self.chat_display.tag_config("user", justify='right')
        else:
            wrapped_message = self.wrap_message(message)
            self.chat_display.insert(tk.END, spacing + wrapped_message + "\n", "bot")
            self.chat_display.tag_config("bot", justify='left')

        self.chat_display.configure(state='disabled')

    def wrap_message(self, message):
        """Wrap the message to fit within the chatbox."""
        char_width = 7
        chat_width = self.chat_display.winfo_width()
        max_line_length = int(chat_width * 0.9 // char_width)

        lines = []
        while len(message) > max_line_length:
            split_point = message.rfind(' ', 0, max_line_length)
            if split_point == -1:
                split_point = max_line_length
            lines.append(message[:split_point])
            message = message[split_point:].lstrip()

        if message:
            lines.append(message)

        return "\n".join(lines)

    # ----- Speech Recognition -----
    def start_speech_recognition(self):
        """Start the speech recognition process."""
        self.handle_voice_input_state(True)

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio)
                self._add_message(f"{user_input}", "user")
                self.user_input.delete(0, tk.END)
                self.user_input.insert(0, user_input)
                self.send_message()
            except sr.UnknownValueError:
                self._add_message("Sorry, I couldn't understand the speech. Please try again.", "bot")
            except sr.RequestError:
                self._add_message("Sorry, there was an error with the speech service.", "bot")
            finally:
                self.handle_voice_input_state(False)

    def handle_voice_input_state(self, state):
        """Centralize the state management for voice input."""
        self.voice_input = state
        self.speech_recognition_active = state

    # ----- Recipe Generation -----
    def generate_response(self, intent, ingredients, allergies, diet):
        """Generate the appropriate bot response based on the user input."""
        if intent == "greet":
            return "Hi! How can I help you?"
        elif intent == "request_recipe":
            return self.handle_recipe_request(ingredients, allergies, diet)
        elif intent == "specify_allergies":
            self.recommender.user_profile["excluded_ingredients"] = allergies
            return "Thanks for sharing your allergies! I'll keep that in mind when suggesting recipes."
        elif intent == "specify_diet":
            self.recommender.user_profile["diet"] = diet
            return "Thanks for letting me know about your diet! I'll filter recipes based on that."
        elif intent == "search_information":
            return "Searching for information..."
        else:
            return "I'm not sure how to help with that."

    def handle_recipe_request(self, ingredients, allergies, diet):
        """Handles the request for recipes."""
        self.recommender.user_profile["excluded_ingredients"] = allergies
        self.recommender.user_profile["diet"] = diet

        recipes = self.recommender.search_recipes(ingredients)
        if recipes:
            # Fetch the details of the first recipe
            first_recipe_details = self.recommender.fetch_recipe_details(recipes[0]['id'])
            
            # Extract recipe details
            recipe_name = first_recipe_details[0]
            recipe_image_url = first_recipe_details[1]
            recipe_ingredients = first_recipe_details[2]
            recipe_instructions = first_recipe_details[3]

            # Construct recipe information text
            recipe_info = f"Recipe: {recipe_name}\n\n"
            recipe_info += "Ingredients:\n"
            for ingredient in recipe_ingredients:
                recipe_info += f"• {ingredient}\n"
            
            recipe_info += "\nInstructions:\n"
            recipe_info += f"{recipe_instructions}\n"

            # Display the recipe image
            if recipe_image_url:
                try:
                    response = requests.get(recipe_image_url)
                    img_data = response.content
                    img = Image.open(BytesIO(img_data))
                    img = img.resize((300, 200))
                    img_tk = ImageTk.PhotoImage(img)

                    self.chat_display.image_create(tk.END, image=img_tk)
                    self.chat_display.image = img_tk

                except Exception as e:
                    self._add_message(f"Could not load image. Error: {e}", "bot")

            # If voice input, convert response to speech
            if self.voice_input:
                self.text_to_speech(recipe_info)

            return recipe_info
        else:
            return "Sorry, I couldn't find any recipes based on your preferences."

    def text_to_speech(self, text):
        """Convert text to speech."""
        def speak():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

        self.master.after(0, speak)

    def clear_chat(self):
        """Clear the chat display."""
        self.chat_display.configure(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state='disabled')

# Running the GUI
if __name__ == "__main__":
    root = tk.Tk()
    chatbot = ChatbotGUI(root)
    root.mainloop()