#!usr/bin/env/python


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from tqdm import tqdm
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU
from tensorflow.keras.layers import Dense, Activation, Dropout, Input
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.losses import CategoricalCrossentropy, SparseCategoricalCrossentropy
from tensorflow.keras.layers import GlobalMaxPooling1D, Conv1D, MaxPooling1D, Flatten, Bidirectional, SpatialDropout1D
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import numpy as np
import tensorflow.compat.v1.keras.backend as K
import tensorflow as tf
tf.compat.v1.disable_eager_execution()



df = pd.read_csv("train.csv")

df["text"]=df["text"].str.lower()


def getLemmText(text):
 tokens=word_tokenize(text)
 lemmatizer = WordNetLemmatizer()
 tokens=[lemmatizer.lemmatize(word) for word in tokens]
 return " ".join(tokens)


def getStemmText(text):
    tokens=word_tokenize(text)
    ps = PorterStemmer()
    tokens=[ps.stem(word) for word in tokens]
    return(' '.join(tokens))



xtrain, xtest, ytrain, ytest = train_test_split( df["text"], df["author"], test_size=0.33, random_state=53)
print(xtrain.shape)
print(xtest.shape)
print(ytrain)

NUM_CLASSES = len(df["author"].unique())
EMBEDDING_DIMENSION = 64
VOCABULARY_SIZE = 2000
MAX_LENGTH = 100
OOV_TOK = '<OOV>'
TRUNCATE_TYPE = 'post'
PADDING_TYPE = 'post'


tokenizer = Tokenizer(num_words=VOCABULARY_SIZE, oov_token=OOV_TOK)
tokenizer.fit_on_texts(list(xtrain) + list(xtest))



xtrain_sequences = tokenizer.texts_to_sequences(xtrain)
xtest_sequences = tokenizer.texts_to_sequences(xtest)
word_index = tokenizer.word_index
print('Vocabulary size:', len(word_index))
dict(list(word_index.items())[0:10])


xtrain_pad = sequence.pad_sequences(xtrain_sequences, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNCATE_TYPE)
xtest_pad = sequence.pad_sequences(xtest_sequences, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNCATE_TYPE)


print(xtrain_pad.shape)

label_tokenizer = Tokenizer()
label_tokenizer.fit_on_texts(list(ytrain))
training_label_seq = np.array(label_tokenizer.texts_to_sequences(ytrain))
test_label_seq = np.array(label_tokenizer.texts_to_sequences(ytest))


reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
def decode_article(text):
 return(' '.join([reverse_word_index.get(i, "?") for i in text]))


xtrain_pad = np.expand_dims(xtrain_pad, axis=1)
print(xtrain_pad.shape)
inputs = Input(shape=(1,xtrain_pad.shape[-1] ))
print(inputs.shape)
x = Bidirectional(GRU(units=128, return_sequences=True, dropout=0.2))(inputs)
print(x.shape)
x = GlobalMaxPooling1D()(x)
outputs = Dense(units=4,activation="softmax")(x)
model = Model(inputs = inputs, outputs=outputs, name="multiclass_GRU")
model.compile(loss=SparseCategoricalCrossentropy(from_logits=True), optimizer="adam", metrics=["accuracy"])
model.summary()


num_epochs = 3
history = model.fit(xtrain_pad, training_label_seq, epochs=num_epochs)
