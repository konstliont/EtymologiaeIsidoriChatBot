import random
import sqlite3
import torch

from model import NeuralNet
from nltkutils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

con = sqlite3.connect("chatbot_liberx.db")
cur = con.cursor()


FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Isidorus Hispalensis"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    cur.execute("SELECT response FROM responses INNER JOIN tags ON responses.tag_id = tags.id WHERE tags.tag = ?", (tag,))
    responses = cur.fetchall()
    if prob.item()>0.75 and responses:
        return random.choice([r[0] for r in responses])

    return "I do not understand or maybe I have not the etymology of this word. You can search into the works of other scholars too..."
