import torch
from transformers import AutoModel, AutoTokenizer
from torch import nn
import data
import random
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

data = data.data

tags = []
labels = []
texts = []
count = 0

for item in data:
  tags.append(item["tag"])

  patterns = item["patterns"]
  for pattern in patterns:
    labels.append(count)
    texts.append(pattern)
  count = count+1

num_class = len(tags)

class BertClassifier(nn.Module):

    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(in_features=128, out_features= 300)
        self.sigmoid = nn.Sigmoid()
        self.linear2 = nn.Linear(300, num_class)

    def forward(self, input_id, mask):
        input_id = input_id.resize_(1, 128)
        input_id = input_id.to(torch.float32)

        linear1_output = self.linear1(input_id)
        sigmoid = self.sigmoid(linear1_output)
        linear2_output = self.linear2(sigmoid)

        return linear2_output

model1 = BertClassifier()
model1.load_state_dict(torch.load("model/model.pth"))

model1.eval()

while(1):
    text = input("#")
    if(text == 'c'):
        break
    else:
        sen = text
        
        sen = sen.lower()
        sen = sen.replace(".", "")

        input_sen = tokenizer(sen,padding='max_length', max_length = 128, truncation=True,return_tensors="pt")
        input_ids = input_sen["input_ids"]
        mask = input_sen["attention_mask"]

        output = model1(input_ids,mask)

        print(random.choice(data[output.argmax(dim=1).item()]["responses"]))