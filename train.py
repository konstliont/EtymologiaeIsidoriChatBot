import numpy as np
import random
import sqlite3

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nltkutils import bag_of_words, tokenize, stem
from model import NeuralNet

con = sqlite3.connect("chatbot_liberx.db") 
cur = con.cursor()               

cur.execute("SELECT id, tag FROM tags")
tags_data = cur.fetchall()

cur.execute("SELECT tag_id, pattern FROM patterns")
patterns_data = cur.fetchall()

cur.execute("SELECT tag_id, response FROM responses")
responses_data = cur.fetchall()

con.close()

tags = [tag[1] for tag in tags_data]  
all_words = []
xy = []

for pattern in patterns_data:
    tag_id, sentence = pattern
    words = tokenize(sentence)
    all_words.extend(words)
    tag = next(tag_name for tag_id_db, tag_name in tags_data if tag_id_db == tag_id)  
    xy.append((words, tag))


ignore_words = ['?', '.', '!']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)


num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
print(input_size, output_size)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)


criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        
        outputs = model(words)
        
        loss = criterion(outputs, labels)
        
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


print(f'final loss: {loss.item():.4f}')

data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')