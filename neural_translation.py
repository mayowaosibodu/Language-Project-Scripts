
from keras.models import Model
from keras.layers import Input, LSTM, Dense
import numpy as np
from keras.models import load_model

import pickle

encoder_model = load_model('encoder_model_2000.h5')
decoder_model = load_model('decoder_model_2000.h5')


max_encoder_seq_length = 241
max_decoder_seq_length = 196
num_encoder_tokens = 79
num_decoder_tokens = 77

with open('input token index.pkl', 'rb') as f:
    input_token_index = pickle.load(f)

with open('target token index.pkl', 'rb') as f:
    target_token_index = pickle.load(f)

with open('reverse target char index.pkl', 'rb') as f:
    reverse_target_char_index = pickle.load(f)



def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)
    print('Encoder prediction: ', states_value[0][0][:5])

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0, target_token_index['\t']] = 1.

    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if (sampled_char == '\n' or
           len(decoded_sentence) > max_decoder_seq_length):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        # Update states
        states_value = [h, c]

    return decoded_sentence





def translate(rus_text):
    encoder_input_data = np.zeros(
        (1, max_encoder_seq_length, num_encoder_tokens),
        dtype='float32')

    for i, input_text in enumerate([rus_text]):
        for t, char in enumerate(input_text):
            encoder_input_data[i, t, input_token_index[char]] = 1.

    # print ('Encoder input: ', encoder_input_data)

    return decode_sequence(encoder_input_data)
