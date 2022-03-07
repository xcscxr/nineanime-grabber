import questionary
from constants import questionary_styles as custom_style

def rawselect(question, choices):
    return questionary.rawselect(
        question,
        choices = choices,
        style=custom_style
    )

def select(question, choices):
    return questionary.select(
        question,
        choices = choices,
        style=custom_style
    )
    
def text_input(text):
    return questionary.text(
        text,
        validate = lambda text: True if len(text) > 0 else "Please enter a value",
        style=custom_style
    )
    
