import torch
from transformers import AutoModel, AutoTokenizer
from torch import nn
from torch.optim import Adam
import numpy as np
from tqdm import tqdm
import data as d

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

data = d.data
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


def train(model, learning_rate=0.0001, epochs=d.n_train):

    train = Dataset()
    train_dataloader = torch.utils.data.DataLoader(
        train, batch_size=1, shuffle=True)

    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=learning_rate)

    for epoch_num in range(epochs):

        total_acc_train = 0
        total_loss_train = 0
        model.train()
        for train_input, train_label in tqdm(train_dataloader):

            mask = train_input['attention_mask']
            input_id = train_input['input_ids']

            output = model(input_id, mask)
            batch_loss = criterion(output, train_label.long())
            total_loss_train += batch_loss.item()

            acc = (output.argmax(dim=1) == train_label).sum().item()
            total_acc_train += acc

            model.zero_grad()
            batch_loss.backward()
            optimizer.step()

            total_acc_val = 0
            total_loss_val = 0
            model.eval()
            with torch.no_grad():
              for val_input, val_label in train_dataloader:
                val_label = val_label
                mask = val_input['attention_mask']
                input_id = val_input['input_ids'].squeeze(1)

                output = model(input_id, mask)

                batch_loss = criterion(output, val_label.long())
                total_loss_val += batch_loss.item()

                acc = (output.argmax(dim=1) == val_label).sum().item()
                total_acc_val += acc

            print(
                f'Epochs: {epoch_num + 1} | Train Loss: {total_loss_train / len(train): .3f} \
                | Train Accuracy: {total_acc_train / len(train): .3f} \
                | Val Loss: {total_loss_val / len(train): .3f} \
                | Val Accuracy: {total_acc_val / len(train): .3f}')


class Dataset(torch.utils.data.Dataset):

    def __init__(self):

        self.labels = labels
        self.texts = [tokenizer(text,
                                padding='max_length', max_length=128, truncation=True,
                                return_tensors="pt") for text in texts]

    def classes(self):
        return self.labels

    def __len__(self):
        return len(self.labels)

    def get_batch_labels(self, idx):
        # Fetch a batch of labels
        return np.array(self.labels[idx])

    def get_batch_texts(self, idx):
        # Fetch a batch of inputs
        return self.texts[idx]

    def __getitem__(self, idx):

        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)

        return batch_texts, batch_y


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

train(model1)

model1.eval()

torch.save(model1.state_dict(), "model/model.pth")
