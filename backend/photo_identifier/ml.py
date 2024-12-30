# food_identifier/ml.py
import random

def run_food_model(image_path):
    """
    Mock ML function to simulate food identification.
    Replace this with your actual ML model inference logic.
    """
    categories = ['Pizza', 'Burger', 'Salad', 'Pasta', 'Sushi']
    prediction = {
        'category': random.choice(categories),
        'confidence': random.uniform(0.6, 0.99)
    }
    return prediction
