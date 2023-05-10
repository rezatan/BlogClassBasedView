import tensorflow as tf
import numpy as np
from PIL import Image

# Load the model
model = tf.keras.models.load_model('static\model')

# Function to preprocess the image and perform prediction
def predict_image(image_file):
    # Preprocess the image
    # Load the image
    image = Image.open(image_file)

    # Resize the image to (150, 150)
    image = image.resize((150, 150))

    # Convert the image to numpy array
    image = np.array(image)

    # Normalize the image
    image = image / 255.0

    # Add extra dimension to match the input shape
    image = np.expand_dims(image, axis=0)

    # Perform prediction
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction)

    # Return the predicted class
    classes = ['Paper', 'Rock', 'Scissors']

    return classes[predicted_class]