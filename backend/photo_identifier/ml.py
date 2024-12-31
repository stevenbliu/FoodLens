# food_identifier/ml.py
import random

def run_food_model(image_path):
    """
    Mock ML function to simulate food identification.
    Replace this with your actual ML model inference logic.
    """
    labels = ['Pizza', 'Burger', 'Salad', 'Pasta', 'Sushi']
    prediction = {
        'label': random.choice(labels),
        'confidence': random.uniform(0.6, 0.99)
    }
    return prediction
