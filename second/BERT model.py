import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForMultipleChoice
from quiz_data_psyc import options
from question_psyc import questions
# Initialize tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMultipleChoice.from_pretrained('bert-base-uncased')

# Psychology questions and options


correct_answers = [1, 3, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 3, 2, 3, 0, 0, 3, 2, 1, 
                   2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 0, 0, 0, 3, 2, 1, 2, 2, 1, 
                   1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 0, 0, 0, 1, 2, 1, 2, 1,
                   1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 0, 0, 0,
                   0, 0, 0, 3, 2, 2, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2,
                   1, 2, 1, 1, 1, 1, 1]  # Assuming these are 0-indexed

class PsychologyDataset(Dataset):
    def __init__(self, questions, options, correct_answers):
        self.questions = questions
        self.options = options
        self.correct_answers = correct_answers

    def __len__(self):
        return len(self.questions)

    def __getitem__(self, idx):
        question = self.questions[idx]
        option = self.options[idx]
        inputs = tokenizer([question] * len(option), option, padding=True, return_tensors="pt")
        label = torch.tensor(self.correct_answers[idx])  # Convert to tensor
        return inputs.input_ids, inputs.attention_mask, label, idx

dataset = PsychologyDataset(questions, options, correct_answers)
dataloader = DataLoader(dataset, batch_size=1)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(15):  # Number of epochs
    total_loss = 0
    correct_predictions = 0
    total_predictions = 0

    for batch in dataloader:
        input_ids, attention_mask, labels, idx = [b.to(device) for b in batch]

        model.zero_grad()  # Reset gradients to zero
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        
        loss = outputs.loss
        logits = outputs.logits
        loss.backward()  # Backpropagation
        optimizer.step()  # Update weights

        total_loss += loss.item()

        # Calculate accuracy
        predictions = torch.argmax(logits, dim=1)
        correct_predictions += (predictions == labels).sum().item()
        total_predictions += labels.size(0)

    # Calculate average loss and accuracy over the epoch
    avg_loss = total_loss / len(dataloader)
    accuracy = correct_predictions / total_predictions

    print(f"Epoch {epoch}, Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")

model.eval()  # Set the model to evaluation mode
correct_count = 0
with torch.no_grad():
    for batch in dataloader:
        input_ids, attention_mask, labels, idx = [b.to(device) for b in batch]
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
        correct = labels.item()
        predicted = predictions.item()
        correct_count += (predicted == correct)
        print(f"Question: {questions[idx]}")
        for i, opt in enumerate(options[idx]):
            pred_indicator = "(Predicted)" if i == predicted else ""
            correct_indicator = "(Correct)" if i == correct else ""
            print(f"Option {i+1}: {opt} {pred_indicator} {correct_indicator}")
        print()

print(f"Total Correct Predictions: {correct_count} out of {len(questions)}")