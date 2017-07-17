# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
from keras.backend.tensorflow_backend import dropout
from strgen import StringGenerator as SG
from keras.models import Sequential
from keras import layers
import keyboard
import time

class colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'

class CharacterTable(object):
    """Given a set of characters:
    + Encode them to a one hot integer representation
    + Decode the one hot integer representation to their character output
    + Decode a vector of probabilities to their character output
    """
    def __init__(self, chars):
        """Initialize character table.
        # Arguments
            chars: Characters that can appear in the input.
        """
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    def encode(self, C, num_rows):
        """One hot encode given string C.
        # Arguments
            num_rows: Number of rows in the returned one hot encoding. This is
                used to keep the # of rows for each data the same.
        """

        x = np.zeros((num_rows, len(self.chars)))
        for i, c in enumerate(C):
            x[i, self.char_indices[c]] = 1
        return x

    def decode(self, x, calc_argmax=True):
        if calc_argmax:
            x = x.argmax(axis=-1)
        return ''.join(self.indices_char[x] for x in x)



def mapper(month):
    months_map = {"01": 'OCA', "02": 'SUB', "03": "MAR", "04": "NIS",
                  "05": "MAY", "06": "HAZ", "07": "AGU", "08": "TEM",
                  "09": "EYL", "10":"EKI", "11":"KAS", "12":"ARA"}
    return months_map.get(month, "OCA")

def read_stateful_user_data():
    fr = open("ml_traces_lstm", 'r')
    max_len = 0
    requests = []
    responses = []
    chars = ""
    while True:
        line1 = fr.readline()
        line2 = fr.readline()
        if not line1 or not line2: break  # EOF
        if len(line1) > max_len:
            max_len = len(line1)
        if len(line2) > max_len:
            max_len = len(line2)
        requests.append(line1.strip().upper())
        responses.append(line2.strip().upper())
        chars += line1.strip().upper()
        chars += line2.strip().upper()
    chars = ''.join(list(set(chars)))
    return chars, max_len, requests, responses

def read_bank_data():
    fr = open("bank_data.xml", 'r')
    max_len = 0
    requests = []
    responses = []
    while True:
        line1 = fr.readline()
        line2 = fr.readline()
        #190 is chosen based on the data
        if len(line1) > 190 or len(line2) >190:
            continue
        if len(line1) > max_len:
            max_len = len(line1)
        if len(line2) > max_len:
            max_len = len(line2)
        if not line1 or not line2: break  # EOF
        requests.append(line1.strip().upper())
        responses.append(line2.strip().upper())
    return max_len, requests, responses


def create_data():
    num = np.random.randint(1, 100)
    tk = "TK%s" % np.random.randint(3, 400)
    th = "%s%s" % (np.random.randint(1, 30), mapper(np.random.randint(1, 12)))
    st = "%s" % SG("[ABCDEFGHIJKLM]{3}").render()
    end = "%s" % SG("[ABCDEFGHIJKL]{3}").render()

    a = "{0}{1}I{2}{3}{4}".format(num, tk, th, st, end)
    b = "1 {1} I {2} {4}{3}".format(num, tk, th, st, end)
    return a, b

# a, b = create_data()


print('Generating data...')

questions = []
expected = []
# MAXLEN, questions, expected = read_bank_data()
chars, MAXLEN, questions, expected = read_stateful_user_data()
chars += '#'
print(chars)
read_stateful_user_data

# Parameters for the model and dataset.
TRAINING_SIZE = len(questions)
DIGITS = MAXLEN+3
INVERT = False

# Maximum length of input is 'int + int' (e.g., '345+678'). Maximum length of
# int is DIGITS.
MAXLEN = DIGITS + 1

# All the numbers, plus sign and space for padding.
# chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-.:\"/=?<># '
ctable = CharacterTable(chars)

for i in range(TRAINING_SIZE):
    questions[i] = questions[i] + '#' * (MAXLEN - len(questions[i]))
    expected[i] = expected[i] + '#' * (MAXLEN - len(expected[i]))

# seen = set()

# while len(questions) < TRAINING_SIZE:

    # a,b = create_data()
    # key = tuple(sorted((a, b)))
    # if key in seen:
    #     continue
    # seen.add(key)

    # query = a + ' ' * (MAXLEN - len(a))
    # ans   = b + ' ' * (MAXLEN - len(b))

    # questions.append(query)
    # expected.append(ans)

print('Total addition questions:', len(questions))
print("question: ", (questions[0]))
print("answer: ", (expected[0]))

print('Vectorization...')
x = np.zeros((len(questions), MAXLEN, len(chars)), dtype=np.bool)
y = np.zeros((len(questions), MAXLEN, len(chars)), dtype=np.bool)

for i, sentence in enumerate(questions):
    x[i] = ctable.encode(sentence, MAXLEN)

for i, sentence in enumerate(expected):
    y[i] = ctable.encode(sentence, MAXLEN)


# Shuffle (x, y) in unison as the later parts of x will almost all be larger
# digits.
indices = np.arange(len(y))
np.random.shuffle(indices)
x = x[indices]
y = y[indices]


# Explicitly set apart 10% for validation data that we never train over.
split_at = len(x) - len(x) // 10
(x_train, x_val) = x[:split_at], x[split_at:]
(y_train, y_val) = y[:split_at], y[split_at:]

print('Training Data:')
print(x_train.shape)
print(y_train.shape)

print('Validation Data:')
print(x_val.shape)
print(y_val.shape)


# Try replacing GRU, or SimpleRNN.
RNN = layers.LSTM
HIDDEN_SIZE = 128
BATCH_SIZE = 64
LAYERS = 2
LSTM_ITERATION = 1000

print('Build model...')
model = Sequential()
# "Encode" the input sequence using an RNN, producing an output of HIDDEN_SIZE.
# Note: In a situation where your input sequences have a variable length,
# use input_shape=(None, num_feature).
model.add(RNN(HIDDEN_SIZE, input_shape=(MAXLEN, len(chars))))
# As the decoder RNN's input, repeatedly provide with the last hidden state of
# RNN for each time step. Repeat 'DIGITS + 1' times as that's the maximum
# length of output, e.g., when DIGITS=3, max output is 999+999=1998.
model.add(layers.RepeatVector(DIGITS+1))
# The decoder RNN could be multiple layers stacked or a single layer.
for _ in range(LAYERS):
    # By setting return_sequences to True, return not only the last output but
    # all the outputs so far in the form of (num_samples, timesteps,
    # output_dim). This is necessary as TimeDistributed in the below expects
    # the first dimension to be the timesteps.
    model.add(RNN(HIDDEN_SIZE, return_sequences=True))

# Apply a dense layer to the every temporal slice of an input. For each of step
# of the output sequence, decide which character should be chosen.
model.add(layers.TimeDistributed(layers.Dense(len(chars))))
model.add(layers.Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

#keyboard.wait("space")


print('TRAIN START')
print("TOTAL ITERATION:", LSTM_ITERATION)
# Train the model each generation and show predictions against the validation
# dataset.
for iteration in range(1, LSTM_ITERATION):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=1,
              validation_data=(x_val, y_val))

    # Select 10 samples from the validation set at random so we can visualize
    # errors.
    for i in range(5):
        ind = np.random.randint(0, len(x_val))
        rowx, rowy = x_val[np.array([ind])], y_val[np.array([ind])]
        preds = model.predict_classes(rowx, verbose=0)
        q = ctable.decode(rowx[0])
        correct = ctable.decode(rowy[0])
        guess = ctable.decode(preds[0], calc_argmax=False)
        print('Q :', q)
        print('A :', correct)

        if correct == guess:
            print(colors.ok + '☑' + colors.close, end=" ")
        else:
            print(colors.fail + '☒' + colors.close, end=" ")

        print(guess)
        print('------------')

    # time.sleep(2)
model.save('stateful_user_data.h5')
