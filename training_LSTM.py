import tensorflow as tf
import random
import numpy as np
import os
from quiz_data_psyc import options
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
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
    "In mood disorders, the term 'etiology' refers to:", #2
    "What is a key feature of Post-Traumatic Stress Disorder (PTSD)?", #1
    "Acute Stress Disorder differs from PTSD primarily in terms of:", #1 
    "Which of the following is a common symptom of Adjustment Disorders?", #1
    "Reactive Attachment Disorder is characterized by:", #1
    "Disinhibited Social Engagement Disorder is most likely to be diagnosed in:", #2
    "What is a key feature of Generalized Anxiety Disorder (GAD)?", #1
    "Panic Disorder is characterized by:", #1
    "Which of the following best describes a phobia?", #2
    "Obsessive-Compulsive Disorder (OCD) involves:", #1
    "Which disorder is characterized by an intense fear of gaining weight and a distorted body image?", #2
    "What is a characteristic feature of Somatic Symptom Disorder?", #0
    "Illness Anxiety Disorder is primarily characterized by:", #0
    "Which of the following is a common treatment approach for mood disorders?", #0
    "What is the primary focus of Module 10 in the textbook?", #3
    "What is a key characteristic of Somatic Symptom Disorder?",#2
    "How is Illness Anxiety Disorder primarily characterized?",#1
    "Which of the following is true about the epidemiology of Somatic Symptom and Related Disorders?", #2
    "What is a common etiological factor for Somatic Symptom and Related Disorders?", #2
    "How do psychological factors affect other medical conditions as per the DSM-5-TR?", #1
    "Adequate sleep is crucial in mental health because it:", #1
    "Group therapy is effective in mental health care because it:", #1
    "Chronic loneliness in mental health is associated with:", #2
    "The use of telepsychiatry in rural areas primarily addresses:", #2
    "Regular physical activity in mental health is linked to:", #2
    "Art therapy in mental health is used to:", #1
     "The impact of cyberbullying on mental health is:", #2
    "Poor work-life balance can affect mental health by:", #2
    "The relationship between nutrition and mental health is evidenced by:", #2
    "In educational settings, mental health initiatives are important because they:",#1
    "Economic stability impacts mental health by:",#1
    "Psychological resilience refers to:",#1
    "Engaging in a digital detox (reducing screen time) can benefit mental health by:", #0
    "Strong personal relationships impact mental health by:", #0
    "Unemployment can affect mental health by:", #0
    "Effective coping strategies in mental health include:", #1
    "The impact of natural disasters on mental health often includes:", #2
    "Mental health stigma varies across cultures, often affecting:", #1
    "In the study of personality disorders, genetics is considered to:", #2
    "Owning a pet can impact mental health by:", #1
     "Self-help approaches in mental health:", #1
    "Veterans returning from war often face mental health challenges such as:",#1
    "Social support in recovery from mental illness:", #1
    "Long-term effects of bullying on mental health can include:", #2
    "School-based mental health interventions are important because they:", #1
     "The relationship between chronic pain and mental health issues is:", #1
    "Active community engagement impacts mental health by:", #1
    "Music therapy in mental health is used to:", #1
    "Workplace discrimination can affect mental health by:", #1
    "Sleep disorders are often associated with:", #2
     "The process of grief can impact mental health by:", #1
    "Improving mental health literacy in the population:", #1
    "Regular exercise is believed to affect cognitive function by:", #2
    "Anxiety related to climate change can lead to:", #2
    "Volunteering is known to impact mental health by:",#1
    "Prolonged social isolation can lead to:", #2
    "The post-pandemic era has seen mental health challenges such as:", #2
     "Negative body image is closely associated with:", #0
    "Financial stress can significantly impact mental health, leading to:", #0
    "Exposure to nature and green spaces is believed to:", #0
    "Effective stress management techniques in mental health are important because they:", #0
    "Different parenting styles can affect a child's mental health by:", #0
    "Excessive use of digital devices and online activities can lead to:", #0
    "Mindfulness techniques are used in mental health to:", #3
     "Job satisfaction can affect mental health by:", #2
    "Early life experiences, such as childhood trauma, can:", #2
    "Excessive academic pressure on students is linked to:", #2
    "Maintaining regular sleep patterns contributes to mental health by:", #2
    "The mental health of parents can:",#1
    "Participation in recreational activities affects mental health by:",#2
    "Members of the LGBTQ+ community face unique mental health challenges due to:",#1
    "Poor work-life integration can lead to:",
    "Caregivers of individuals with chronic illnesses often experience:",
    "Cyberpsychology, the study of the human mind and behavior in the context of digital technology, primarily explores:",
    "Long-term hospitalization can impact mental health by potentially causing:",
    "Trauma-informed care in mental health focuses on:",
    "A consistent daily routine can affect mental health by:",
    "Personal growth and development can contribute to mental health by:",
    "In higher education settings, mental health issues are often related to:",
    "Living in urban areas can influence mental health due to factors like:",
    "Experiencing discrimination can affect mental health by leading to:",
    "Gardening can impact mental health by:",
    "Increasing mental health awareness in the workplace can lead to:",
    "Pets can contribute to mental health management by:",
    "Engagement with arts and culture can affect mental health by:",
    "Yoga and meditation are used in mental health to:",
    "Mental health challenges in retirement can include:",









]





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

    epochs=4,  # You can set a higher number of epochs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~))))))))))))))))))))))))

    batch_size=88,
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

# Convert predictions to labels
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

