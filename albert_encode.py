import transformers
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Dropout, GlobalMaxPooling1D
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from transformers import AutoTokenizer, ElectraTokenizerFast, TFElectraModel, TFAlbertModel, TFBertModel
#from transformers import BertModel, BertForMaskedLM
#.modeling_bert
from tensorflow.keras import Model
import numpy as np
import json
import time
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences



#######################
# data stuffs       ###
#######################



text_data = tfds.load('imdb_reviews', split=['train', 'test'])

#Create empty lists to hold our training and test text and labels
train_text = []
train_labels = []
test_text = []
test_labels = []

#Iterate over the imdb data set and add text + labels to their respective list variables
for row in text_data[0]: #training set
    #takes just the first 20 words from the review
    train_text.append(row['text'].numpy().decode('utf-8').split()[:20])
    train_labels.append(row['label'].numpy())

for row in text_data[1]: #testing set
    #takes just the first 20 words from the review
    test_text.append(row['text'].numpy().decode('utf-8').split()[:20])
    test_labels.append(row['label'].numpy())


#prints a samples from the training set
print("FIRST 5 SAMPLES OF TRAINING DATA")
print("============================================================")
for i in range(5):
    review = "POSITIVE" if train_labels[i] == 1 else "NEGATIVE"
    print("REVIEW SENTIMENT:", review)
    print("REVIEW TEXT:", " ".join(train_text[i]))
    print("============================================================")

#######################
#  Keras Tokenizer  ###
#######################

tokenizer = Tokenizer(num_words=10_000, oov_token='<OOV>')
tokenizer.fit_on_texts(train_text)

#Creates sequences of numeric representations of words
training_sequences = tokenizer.texts_to_sequences(train_text)
#pads sequences so they all have the same length
training_sequences = pad_sequences(training_sequences, maxlen=20)

#Process test data in the same way for later evaluation
testing_sequences = tokenizer.texts_to_sequences(test_text)
testing_sequences = pad_sequences(testing_sequences, maxlen=20)


#prints a sample of the new sequences
print('PROCESSED TEXT DATA')
print('=========================')
for i in range(5):
    print(training_sequences[i], '\n')




######################
# Hyper parameters ###
######################

AUTO = tf.data.experimental.AUTOTUNE
EPOCHS = 1
MAX_LEN = 20


model_dir = "code"
#MODEL = "google/electra-small-discriminator" #change to albert maybe
#MODEL = "bert-base-cased"
MODEL = "albert-base-v1"
#model_dir = "code"
OPTIMIZER = tf.keras.optimizers.Adam()




#######################
## Model architecture #
#######################



# x = tf.random.uniform(shape=(1,4,2))
#electra = TFElectraModel.from_pretrained(MODEL)
#x = electra(input_ids)[0]
albert = TFAlbertModel.from_pretrained(MODEL)
input_ids = Input(shape=(MAX_LEN, ), dtype=tf.int32)
x = albert(input_ids)[0]
#x = GlobalMaxPooling1D()(bert(input_ids)[0])
#print(x)
#(None, 512,256)
#x = bert(input_ids)[0]
    # options here include attention, last hidden state, global pooling
    # this is arbitrarily the first hidden state
x = x[:, -1, :] # this is the arbitrary last hidden state
#x = GlobalMaxPooling1D()(x)
x = Dropout(0.5)(x)
x = Dense(1, name="output")(x)
model = Model(inputs=input_ids, outputs=x)
model.compile(
loss = tf.losses.BinaryCrossentropy(from_logits=True),
metrics=[tf.metrics.Accuracy()],
optimizer=OPTIMIZER
)
model.summary()








#################
# MODEL loading #
#################


callback = ModelCheckpoint(filepath=model_dir, monitor="val_loss",
            save_weights_only=False, model="auto",save_freq="epoch")


scheduler = ReduceLROnPlateau(monitor="val_loss")


history = model.fit(x=np.array(training_sequences),
                    y=np.array(train_labels),
                    epochs=1)

scores = model.evaluate(x=np.array(testing_sequences),
                        y=np.array(testing_labels))
