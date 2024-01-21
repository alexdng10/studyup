import tensorflow as tf
import random
import numpy as np
import os
import json
from flask import Flask, request, jsonify


tf.config.set_visible_devices([], 'GPU')

# Disable all GPUs
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# Define the maximum length for questions and options
max_question_length = 100  # You may adjust this length based on your actual data
max_option_length = 100  # You may adjust this length as well

# Example data
questions = [
    "What is a primary focus of abnormal psychology?",# 1
    "Which aspect is NOT typically included in the definition of abnormal behavior?", #3
    "What historical perspective did the DSM-5-TR mainly emphasize in defining abnormal behavior?", #1
    "Which of the following best describes 'stigma' in the context of mental illness?",#2
    "What is the role of epidemiology in the field of abnormal psychology?",# 1
    "Which model in abnormal psychology emphasizes the role of unconscious processes and early life experiences?",#1
    "The Biological Model of abnormal psychology primarily focuses on:", #2
    "Which of the following best describes the Cognitive-Behavioral Model?", #2
    "In the Sociocultural Model, mental disorders are understood through:", #2
    "The Humanistic Model in abnormal psychology stresses:", #1
    "What is the primary goal of clinical assessment in abnormal psychology?", #1
    "Which of the following is a key component of clinical assessment?", #1
    "Which of the following is a symptom commonly associated with anxiety disorders?",#3
    "In post-traumatic stress disorder (PTSD), what type of intrusive symptoms may individuals experience?",#2
    "What is a common characteristic of obsessive-compulsive disorder (OCD)?",#3 
    "What is a common characteristic of bipolar mood disorders?",#0
    "Which of the following is a common feature of mood disorders?", #0
    "Which of the following is a symptom commonly associated with anxiety disorders?",#3
    "Which of the following is true about comorbidity in mood disorders?", #2
    "A major depressive episode is NOT typically characterized by:", #1
    "In mood disorders, the term 'etiology' refers to:" #2



    
]

options = [
    ["Studying normal and adaptive behaviors", "Investigating abnormal behavior and mental disorders", "Focusing only on psychological treatments", "Analyzing physical health and well-being"],
    ["Dysfunction", "Distress", "Deviance", "Dependability"],
    ["Sociocultural context", "Biological factors", "Psychological processes", "Environmental influences"],
    ["A form of treatment", "A type of psychological assessment", "A negative belief or attitude towards mental illness", "A classification of mental disorders"],
    [
        "Designing psychological tests",
        "Studying the frequency and causes of mental disorders",
        "Providing therapeutic interventions",
        "Developing new psychotropic medications"
    ],
    [
        "Cognitive-Behavioral Model",
        "Psychodynamic Model",
        "Biological Model",
        "Humanistic Model"
    ],
    [
        "Family and cultural influences",
        "Learned behaviors and cognitive processes",
        "Brain structures, neurotransmitters, and genetics",
        "Self-actualization and personal growth"
    ],
    [
        "It focuses on the individual's social context.",
        "It examines the role of unconscious conflicts.",
        "It emphasizes the influence of thoughts and behaviors.",
        "It considers the biological underpinnings of behavior."
    ],
    [
        "Neural circuits and hormonal imbalances.",
        "Reinforcement and observational learning.",
        "Cultural, social, and familial contexts.",
        "Internal psychological processes."
    ],
    [
        "The impact of genetics on behavior.",
        "The search for meaning and self-direction.",
        "The influence of neurotransmitters.",
        "The role of reinforcement in learning."
    ],
    [
        "To prescribe medication",
        "To understand and predict behavior",
        "To provide psychotherapy",
        "To research new psychological theories"
    ],
    [
        "Psychoanalysis",
        "Psychometric testing",
        "Group therapy sessions",
        "Pharmacological trials"
    ],
    [
        "Persistent changes in appetite or weight",
        "Consistent high energy levels",
        "Avoidance of specific situations or objects",
        "Frequent hallucinations "
    ],
    [
        "Excessive joy and excitement",
        "Consistent low energy levels",
        "Intrusive memories and flashbacks ",
        "Lack of interest in social activities"
    ],
    [
        "Lack of repetitive behaviors or thoughts",
        "Persistent changes in appetite or weight",
        "A complete absence of anxiety",
        "Recurrent and distressing obsessions and compulsions"
    ],
    [
        "Periods of depression followed by periods of mania ",
        "Consistent low energy levels",
        "Lack of interest in social activities",
        "Frequent hallucinations"
    ],
    [
        "Persistent changes in appetite or weight",
        "Consistent high energy levels",
        "Lack of interest in social activities",
        "Frequent hallucinations"
    ],
    [
        "Persistent changes in appetite or weight",
        "Consistent high energy levels",
        "Avoidance of specific situations or objects",
        "Frequent hallucinations"
    ],
    [
        "It is rare in mood disorders",
        "It usually involves only physical health issues",
        "It refers to the presence of one or more additional disorders",
        "It decreases the severity of mood disorders"
    ],
    [
        "Feelings of worthlessness",
        "Increased interest in daily activities",
        "Significant weight loss or gain",
        "Insomnia or hypersomnia"
    ],
    [
        "The process of diagnosing the disorder",
        "The treatment and management of the disorder",
        "The underlying causes and contributing factors of the disorder",
        "The prognosis and outcome of the disorder"
    ],

  
  
]




correct_answers = [1, 3, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 3, 2, 3, 0, 0, 3, 2, 1, 2]  # Indices of the correct answers (0-indexed)
num_questions = len(questions)  # 5 questions
num_options = len(options[0]) 

max_question_length = 150
max_option_length = 150

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

# Prepare training data--------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

# Training
model_input = [all_question_seqs] + [all_option_seqs for _ in range(num_options)]
model.fit(model_input, correct_answers_repeated, epochs=3, batch_size=2)


predictions = model.predict(model_input)

# Convert predictions to labels
predicted_labels = np.argmax(predictions, axis=1)

correct_count = 0  # Initialize a counter for correct predictions

for i in range(len(questions)):
    print(f"Question {i+1}: {questions[i]}")
    for j, option in enumerate(options[i]):
        # Indicate which option is predicted and which one is actual
        pred_indicator = "(Predicted)" if j == predicted_labels[i] else ""
        actual_indicator = "(Correct)" if j == correct_answers[i] else ""
        print(f"  {chr(97 + j)}. {option} {pred_indicator} {actual_indicator}")

    # Check if the prediction was correct and update the counter
    if predicted_labels[i] == correct_answers[i]:
        correct_count += 1

    print()

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