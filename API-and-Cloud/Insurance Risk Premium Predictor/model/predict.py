import os
import pickle
import pandas as pd

# Load the trained model from the pickle file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "model.pkl")

with open(model_path, "rb") as file:
    model = pickle.load(file)

model_version = "1.0.0"

class_labels = model.classes_.tolist()  #['high', 'low', 'medium']

def predict_output(input_data: pd.DataFrame) -> str:
    """
    Predict the health risk category based on the input data.

    Args:
        input_data (pd.DataFrame): A DataFrame containing the input features.

    Returns:
        str: The predicted health risk category.
    """
    try:
        prediction = model.predict(input_data)[0]

        #getting probabilities for each class and confidence score for the predicted class
        probabilities = model.predict_proba(input_data)[0]
        confidence_score = probabilities[class_labels.index(prediction)]
        return {"risk_category": prediction, "confidence_score": confidence_score, "probabilities": dict(zip(class_labels, probabilities))}
    
    except Exception as e:
        raise RuntimeError(f"Error during prediction: {e}")


