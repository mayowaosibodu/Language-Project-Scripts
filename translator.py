
'''Script to train Statistical Machine Translation Model on Parallel corpus.
To build a language translator given a parralel corpus- in this case,
the Russian-Chirag corpus extracted from the University of London's
Endangered Language Archive (ELAR).

Portion commented out splits the data into training, validation, and test sets,
which were used to build a Neural Machine Translation model.'''



from nltk.translate.ibm5 import IBMModel5
from nltk.translate.ibm2 import IBMModel2
from nltk.translate.api import AlignedSent
import os, random, pickle


path = 'Language Project/Chirag Data/'
dir = os.listdir(path)

# for f in dir:

def read_sentences(filename):

    path = 'Language Project/Chirag Data/'
    f = filename
    print ('Processing', f)

    file_io = open(path+f, 'r', encoding="utf-8")
    file_content = file_io.readlines()
    file_io.close()
    # print(len(file_content))


    sentences = []
    for line in file_content:
        line = line.encode('utf8')
        # sentences.append(line)#.split()) Instead of the next line for script to slice files into train, val, etc.
        sentences.append(line.split())
        # I think the newline characters are still in the lines. Full stops also (more probably)

    return sentences

cyrillic = read_sentences('cyrillic.txt')#[:50]
russian = read_sentences('russian.txt')#[:50]



# Script to slice files into train, val, etc.
# def join(array):
#     string = b''
#     for i in array:
#         # print(i)
#         string+= i#+b'\n'
#     return string
#
# print('Working on files...')
#
# cy_train = cyrillic[:int(0.895*len(cyrillic))]
# with open(path+'cy-train.txt', 'wb') as f:
#     # print(join(cy_train))
#     f.write(join(cy_train))
#
# cy_val = cyrillic[int(0.895*len(cyrillic)):int(0.995*len(cyrillic))]
# with open(path+'cy-val.txt', 'wb') as f:
#     f.write(join(cy_val))
#
# cy_test = cyrillic[int(0.995*len(cyrillic)):]
# with open(path+'cy-test.txt', 'wb') as f:
#     f.write(join(cy_test))
#
#
# ru_train = russian[:int(0.895*len(russian))]
# with open(path+'ru-train.txt', 'wb') as f:
#     f.write(join(ru_train))
#
# ru_val = russian[int(0.895*len(russian)):int(0.995*len(russian))]
# with open(path+'ru-val.txt', 'wb') as f:
#     f.write(join(ru_val))
#
# ru_test = russian[int(0.995*len(russian)):]
# with open(path+'ru-test.txt', 'wb') as f:
#     f.write(join(ru_test))
#
# print('Done.')



print('Length of cyrillic', len(cyrillic))
print('Length of russian', len(russian))


aligned_text = []

for i in range(len(cyrillic)):
    aligned_sentence = AlignedSent(russian[i],cyrillic[i])
    aligned_text.append(aligned_sentence)


print(" \nTraining SMT model")
ibm_model = IBMModel2(aligned_text,10)
print("Training complete")

print('Saving Model...')
with open(path+'translation model.pkl', 'w') as tr_io:
    pickle.dump(ibm_model, tr_io)
print('Done.')


n_random = random.randint(0,len(cyrillic)-1)
russian_sentence = russian[n_random]
cyrillic_actual_translation = cyrillic[n_random]

tr_sent = []
for w in russian_sentence:
    probs = ibm_model.translation_table[w]
    if(len(probs)==0):
        continue
    sorted_words = sorted([(k,v) for k, v in probs.items()],key=lambda x: x[1], reverse=True)
    top_word = sorted_words[1][0]
    if top_word is not None:
        tr_sent.append(top_word)

print('\n \nWriting translations to file...')
rus_io = open(path+'Translation Test/russian sentence.txt', 'wb')
rus_io.write(b" ".join(russian_sentence))
rus_io.close()
# print("Russian sentence: ", b" ".join(russian_sentence))

cyr_io = open(path+'Translation Test/machine cyrillic translation.txt', 'wb')
cyr_io.write(b" ".join(tr_sent))
cyr_io.close()
# print("Translated Cyrillic sentence: ", b" ".join(tr_sent))

tra_io = open(path+'Translation Test/original cyrillic translation.txt', 'wb')
tra_io.write(b" ".join(cyrillic_actual_translation))
tra_io.close()
# print("Original translation: ", b" ".join(cyrillic_actual_translation))

print('Done.')
