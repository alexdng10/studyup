import tensorflow as tf
import random
import numpy as np
import os
from flask_cors import CORS
from quiz_data_psyc import options
from question_psyc import questions
from tensorflow.keras.callbacks import EarlyStopping
print("EarlyStopping imported successfully")
from tensorflow.python.framework.test_util import is_gpu_available
print("Is GPU available:", is_gpu_available())
from sklearn.model_selection import train_test_split
import json
from flask import Flask, request, jsonify
from transformers import BertTokenizer, TFBertModel
tf.config.list_physical_devices()




# Simple test operation







correct_answers = [1, 3, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 3, 2, 3, 0, 0, 3, 2, 1, 
                   2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 0, 0, 0, 3, 2, 1, 2, 2, 1, 
                   1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 0, 0, 0, 1, 2, 1, 2, 1,
                   1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 0, 0, 0,
                   0, 0, 0, 3, 2, 2, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2,
                   1, 2, 1, 1, 1, 1, 1]  # Indices of the correct answers (0-indexed)
num_questions = len(questions)  # 5 questions
num_options = len(options[0]) 

max_question_length = 500
max_option_length = 500

# Tokenize the text
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(questions + [opt for sublist in options for opt in sublist])

# Convert to sequences and pad
question_seqs = tokenizer.texts_to_sequences(questions)
question_seqs_padded = tf.keras.preprocessing.sequence.pad_sequences(question_seqs, maxlen=max_question_length)
option_seqs_padded = [tf.keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences(opts), maxlen=max_option_length) for opts in options]

# Model building
embedding_dim = 64
question_input = tf.keras.Input(shape=(max_question_length,), dtype='int32', name='question_input')
option_inputs = [tf.keras.Input(shape=(max_option_length,), dtype='int32', name=f'option_input_{i}') for i in range(4)]

embedding = tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_dim)
question_embedding = embedding(question_input)
option_embeddings = [embedding(option_input) for option_input in option_inputs]

question_lstm = tf.keras.layers.LSTM(embedding_dim)(question_embedding)
option_lstms = [tf.keras.layers.LSTM(embedding_dim)(option_embedding) for option_embedding in option_embeddings]

concatenated_layers = [tf.keras.layers.concatenate([question_lstm, option_lstm]) for option_lstm in option_lstms]
concatenated_all_options = tf.keras.layers.concatenate(concatenated_layers)
dense_layer = tf.keras.layers.Dense(embedding_dim, activation='relu')(concatenated_all_options)
output = tf.keras.layers.Dense(len(options[0]), activation='softmax')(dense_layer)

model = tf.keras.Model(inputs=[question_input] + option_inputs, outputs=output)

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#~~~~~~~********************************************************************************************************************************************************************************************************
# Prepare training data--------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Preparing the question and option sequences
all_question_seqs = []
all_option_seqs = []

for q_idx in range(num_questions):
    question_seq = tokenizer.texts_to_sequences([questions[q_idx]])
    question_seq_padded = tf.keras.preprocessing.sequence.pad_sequences(question_seq, maxlen=max_question_length)
    
    for opt_idx in range(num_options):
        option_seq = tokenizer.texts_to_sequences([options[q_idx][opt_idx]])
        option_seq_padded = tf.keras.preprocessing.sequence.pad_sequences(option_seq, maxlen=max_option_length)

        # Repeat each question sequence and option sequence
        all_question_seqs.append(question_seq_padded)
        all_option_seqs.append(option_seq_padded)

# Convert lists to numpy arrays
all_question_seqs = np.vstack(all_question_seqs)
all_option_seqs = np.vstack(all_option_seqs)

# Repeat the correct answers
correct_answers_repeated = np.repeat(correct_answers, num_options)

# Check the dimensions
print("Questions shape:", all_question_seqs.shape)
print("Options shape:", all_option_seqs.shape)
print("Correct answers shape:", correct_answers_repeated.shape)



train_questions, val_questions, train_answers, val_answers = train_test_split(
    all_question_seqs, correct_answers_repeated, test_size=0.2, random_state=42
)
train_input = [train_questions] + [train_questions for _ in range(num_options)]
val_input = [val_questions] + [val_questions for _ in range(num_options)]


early_stopping = EarlyStopping(
    monitor='val_loss',  # Monitor validation loss
    patience=3,         # Number of epochs with no improvement after which training will be stopped
    restore_best_weights=True  # Restores model weights from the epoch with the lowest validation loss
)


# Training**********************************************************************************************************
model_input = [all_question_seqs] + [all_option_seqs for _ in range(num_options)]
model.fit(
    train_input, 
    train_answers, 

    epochs=10,  # You can set a higher number of epochs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~))))))))))))))))))))))))

    batch_size=32,
    validation_data=(val_input, val_answers),
    callbacks=[early_stopping]
)



import matplotlib.pyplot as plt

# Assuming your model's history attribute is correctly updated
# Plot training & validation accuracy values
plt.plot(model.history.history['accuracy'])
plt.plot(model.history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(model.history.history['loss'])
plt.plot(model.history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()




predictions = model.predict(model_input)


# Convert predictions to option indices
predicted_labels = np.argmax(predictions, axis=1)

correct_count = 0  # Initialize a counter for correct predictions

#look into the print remove the hashtag to print all the questions and stuff
for i in range(len(questions)):
    #print(f"Question {i+1}: {questions[i]}")
    for j, option in enumerate(options[i]):
        # Indicate which option is predicted and which one is actual
        pred_indicator = "(Predicted)" if j == predicted_labels[i] else ""
        actual_indicator = "(Correct)" if j == correct_answers[i] else ""
        #print(f"  {chr(97 + j)}. {option} {pred_indicator} {actual_indicator}")

    # Check if the prediction was correct and update the counter
    if predicted_labels[i] == correct_answers[i]:
        correct_count += 1

    #print()



# Print the total number of correct predictions

print(f"Total Correct Predictions: {correct_count} out of {len(questions)}")

correctly_answered_questions = []
correctly_answered_options = []

for i in range(len(questions)):
    if predicted_labels[i] == correct_answers[i]:
        correctly_answered_questions.append(questions[i])
        correctly_answered_options.append(options[i])

def generate_quiz(questions, options, num_questions=5):
    quiz_questions = random.sample(list(zip(questions, options)), min(num_questions, len(questions)))

    for i, (question, opts) in enumerate(quiz_questions, 1):
        print(f"Question {i}: {question}")
        shuffled_options = random.sample(opts, len(opts))
        for j, opt in enumerate(shuffled_options):
            print(f"  {chr(97 + j)}. {opt}")
        print()

# Generate a quiz with 5 questions
generate_quiz(correctly_answered_questions, correctly_answered_options, num_questions=5)


class QuizNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = QuizNode(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

def get_question(data):
    return data["question"]

def get_options(data):
    return data["options"]

def get_correct_index(data):
    return data["correct_index"]

def generate_quiz_data(questions, options, correct_answers, num_questions=5):
    quiz_data = []
    quiz_questions = random.sample(list(zip(questions, options, correct_answers)), min(num_questions, len(questions)))

    for question, opts, correct_ans in quiz_questions:
        shuffled_options = random.sample(opts, len(opts))
        correct_index = shuffled_options.index(opts[correct_ans])
        quiz_data.append({
            "question": question,
            "options": shuffled_options,
            "correct_index": correct_index
        })

    return quiz_data

# Example usage
quiz_data = generate_quiz_data(correctly_answered_questions, correctly_answered_options, correct_answers, num_questions=5)

# Creating a linked list and populating it with quiz data
quiz_list = LinkedList()
for data in quiz_data:
    quiz_list.append(data)

# Example of using the functions
current_node = quiz_list.head
while current_node:
    print("Question:", get_question(current_node.data))
    print("Options:", get_options(current_node.data))
    print("Correct Index:", get_correct_index(current_node.data))
    print()
    current_node = current_node.next

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/quiz")
def get_questions():
    return jsonify(generate_quiz_data(correctly_answered_questions, correctly_answered_options, correct_answers, num_questions=5)), 200

if __name__== "__main__":
    app.run(debug=True)

