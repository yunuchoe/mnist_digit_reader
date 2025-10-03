import torch
import torch.nn as nn
import torchvision.transforms as transforms
import io

from PIL import Image

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.input_size = input_size
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(hidden_size, num_classes)  
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        return out
    
# Hyper-parameters 
input_size = 784 #28x28 pixels size of MNIST
hidden_size = 500 
num_classes = 10

model = NeuralNet(input_size, hidden_size, num_classes)

PATH = "mnist_ffn.pth" # previous training
model.load_state_dict(torch.load(PATH))
model.eval()

# convert raw image bytes to tensor
def transform_image(image_bytes):
    # single chanel
    # image 28x28 as outlined above
    # convert to PyTorch tensor
    # mean / standard of dev.
    transform = transforms.Compose([transforms.Grayscale(num_output_channels=1), transforms.Resize((28, 28)), transforms.ToTensor(), transforms.Normalize((0.1307,),(0.3081,))])

    image = Image.open(io.BytesIO(image_bytes))

    return transform(image).unsqueeze(0)

# predict
def get_prediction(image_tensor):
    images = image_tensor.reshape(-1, 28*28) # resahpe to 28x28
    output = model(images)
    
    probabilities = torch.softmax(output, dim = 1)
    confidence, predicted = torch.max(probabilities, 1)

    return predicted.item(), confidence.item()