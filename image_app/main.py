from flask import Flask, request, jsonify
from torch_utils import transform_image, get_prediction

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # check POST - only one we care about for this project
    if request.method == 'POST':
        #variables
        file = request.files.get('file') # file itself
        filename = file.filename.lower() # filename

        # error check
        if file is None: # no file
            return jsonify({'error': 'no file found'})
        elif filename == "": # no file name
            return jsonify({'error': 'no file name'})
        elif not filename.lower().endswith(('.png', '.jpg', '.jpeg')): # file type must end in .png .jpg .jpeg
            return jsonify({'error': 'illegal file format'})
        
        try:
            image = file.read()
            tensor = transform_image(image) # convert to tensor
            predicted, confidence = get_prediction(tensor) # predict

            result = { 'prediction': predicted, 'confidence': confidence}
            return jsonify(result)
        except:
            return jsonify({'error': 'error during predictions'})
        
# server
if __name__ == "__main__":
    app.run(debug = True, port = 5000)