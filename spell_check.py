import os, csv, pandas as pd, string
from nltk.metrics import edit_distance as ed

word_dict = {
    'the': 1,
    'beautiful': 2,
    'ducks': 3,
    'swam': 4,
    'in': 5,
    'big': 6,
    'blue': 7,
    'lake': 8,
    'their': 9,
    'feathers': 10,
    'were': 11,
    'very': 12,
    'pretty': 13,
    'and': 14,
    'quite': 15,
    'often': 16,
    'would': 17,
    'jump': 18,
    'out': 19,
    'of': 20,
    'water': 21,
}
word_dict_key = list(word_dict.keys())
sim_con = {
    'b': ['d','h','q','p'],
    'd': ['b', 'h', 'q','p'],
    'h': ['b', 'd', 'q', 'p'],
    'q': ['b', 'd', 'h', 'p'],
    'p': ['b', 'd', 'h', 'q'],
    'f': ['t'],
    't': ['f'],
}
sim_vow = {
    'o': ['u', 'e'],
    'i': ['e'],
    'a': ['e'],
    'e': ['i', 'a', 'u']
}
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
vowels = ['a', 'e', 'i', 'o', 'u']
# print(word_dict_key)
def sim_characters(src, tgt):
    score = []
    phe = 0
    unv = 0
    aee = 0
    doc = 0

    # if length of src and tgt is same but the error is in character
    if len(src) == len(tgt):
        for c in range(len(src)):

            if src[c] != tgt[c]:
                # phonetic error [6]
                if src[c] in sim_con.keys() and tgt[c] in sim_con[src[c]]: phe += 1

                #unstressed vowel [10]
                elif src[c] in sim_vow.keys() and tgt[c] in sim_vow[src[c]]: unv += 1

    # if length of tgt is greater, meaning the child has written extra character
    elif len(src) < len(tgt):
        
        prev_c = ''
        for c in range(len(tgt)):

            # adding extra e [1]
            if c == len(tgt) - 1:
                if tgt[-1] == 'e' and src[-1] != 'e': aee += 1

            if c < len(src):
                #phonetic error [6]
                if src[c] in sim_con.keys() and tgt[c] in sim_con[src[c]]: phe += 1
                
                #doubling of consonants [3]
                if src[c] != tgt[c] and tgt[c] == prev_c and tgt[c] in consonants: doc += 1
                elif src[c] == tgt[c]: prev_c = src[c]

    return phe, unv, aee, doc

def scoring(df):

    sentence_length = list()
    PHE = []    #phonetic error [6]
    UNV = []    #unstressed vowel [10]
    AEE = []    #added extra e [1]
    DOC = []    #doubling of consonants [3]

    for ind, row in df.iterrows():
        phe, unv, aee, doc = 0, 0, 0, 0
        words = row['sentence'].translate(str.maketrans('','',string.punctuation)).lower()
        words = words.split()
        
        #length of sentence
        if len(words) == 25: sentence_length.append(0)
        else: sentence_length.append(abs(len(words)-25))

        for word in words:
            src = ''
            tgt = word
            min_dist = 999

            # edit distance to find the closest word if there are spelling errors
            for x in word_dict_key:
                dist = ed(word, x)
                if dist < min_dist:
                    min_dist = dist
                    src = x
            if min_dist > 0:   # there is an error 
                a, b, c, d = sim_characters(src, tgt)
                phe += a
                unv += b
                aee += c
                doc += d
            
        PHE.append(phe)
        UNV.append(unv)
        AEE.append(aee)
        DOC.append(doc)

    df['sentence length'] = sentence_length
    df['phonetic error'] = PHE
    df['unstressed vowel'] = UNV
    df['adding extra e'] = AEE
    df['doubling consonant'] = DOC
    
    return df

#1: there is error
#0: no error

df = pd.read_csv('data.csv')
df = scoring(df)
df.to_csv('data.csv', index=False)
print(df)
