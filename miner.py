'For some reason, this only works with Python2- Python3 gives some weird ASCII error.'

'''Mines the downloaded Chirag traanscription .eaf files to extract a Russian-Chirag parralel corpus.'''
import os

path = 'Language Project/Chirag Data/Annotations/'
# path = 'Annotations/'

dir = os.listdir(path)



def process(content, annotations):

    ccount = rcount = 0
    content = content[content.find('tx-cyr'):]

    temp = {'cyrillic':'', 'russian':''}

    while '<ANNOTATION_VALUE>' in content:
        rus_index = content.find('ft-ru')
        beginning = content.find('<ANNOTATION_VALUE>')+18

        if beginning< rus_index:
            mode = 'cyrillic'
            ccount += 1
        else:
            mode = 'russian'
            rcount += 1

        text = content[beginning:content.find('</ANNOTATION_VALUE>')]
        # print 'Mode: ', mode
        # print text
        temp[mode] += text+'.\n'
        # annotations[mode] += text+'.\n'

        content = content[content.find('</ANNOTATION_VALUE>')+19:]

    #Filter out annotation files with unequal Cyrillic and Russian sentences.
    if ccount != rcount:
        print 'Number of sentences in the two languages are unequal, ', ccount, 'and', rcount, '.'
        print 'Not adding to annotations.'
    else:
        for key in temp:
            annotations[key] += temp[key]

    return annotations




results = {'cyrillic':'', 'russian':''}

for f in dir:
# for f in ['chirag0001.eaf']:

    if f != '.DS_Store':
        print 'Processing', f

        file_io = open(path+f, 'r')
        file_content = file_io.read()
        file_io.close()

        results = process(file_content, results)

        # print 'Done.'

russian_io = open('Language Project/Chirag Data/russian.txt', 'w')
russian_io.write(results['russian'])
russian_io.close()

cyrillic_io = open('Language Project/Chirag Data/cyrillic.txt', 'w')
cyrillic_io.write(results['cyrillic'])
cyrillic_io.close()
