# -*- coding: utf-8 -*-
#
# Extracts features from app descriptions
#
# Processes app descriptions and then extracts features by using NLTK to find bi/trigrams
# and hierarchical clustering to find core features and alternative tokens
#
# Based off of NLP_Functions.py by Homayoon Farrahi

import csv
import nltk
import os
import re
import shutil

from pattern.vector import Cluster, COSINE, Document, HIERARCHICAL, Model

INPUT_PATH = 'output/apps'
OUTPUT_PATH = 'output/features'


def extract():
    print 'Extracting features from app descriptions...\n'
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    for dir in os.listdir(INPUT_PATH):
        if not dir.startswith('.'):
            os.makedirs("{}/{}".format(OUTPUT_PATH, dir))
            for file in os.listdir('{}/'.format(INPUT_PATH) + dir):            
                with open('{}/{}/{}'.format(INPUT_PATH, dir, file), 'rb') as f:
                    reader = csv.reader(f)
                    next(reader)
                    with open('{}/{}/{}'.format(OUTPUT_PATH, dir, file), 'wb') as r:
                        writer = csv.writer(r)
                        for app in reader:
                            name = app[0]
                            description = app[2]

                            # Prepare an app description string for NLTK and LDA processing
                            preparedDescription = prepare_description(description)

                            # Extract 3 word featurlets from the description
                            featurelets = featurelet_extraction(preparedDescription)

                            list = []
                            for feature in featurelets:
                                featurelet = '{} {} {}'.format(feature[0], feature[1], feature[2])
                                list.append(Document(featurelet, name=featurelet))

                            # Perform hierarchical clustering
                            m = Model(list)
                            cluster = m.cluster(method=HIERARCHICAL, k=3, iterations=1000, distance=COSINE)

                            # Organize clusters into features and alternative tokens
                            (features, alterTokens) = group(cluster, [], [], [])

                            # Write results to file
                            writer.writerow([name, description, features, alterTokens])
                        r.close()
                    f.close()


def group(cluster, features, alterTokens, unique):
    for c in cluster:
        if type(c) == Document:
            unique = c.name.split(' ')
        else:
            if c.depth > 0:
                group(c, features, alterTokens, [])
            else:
                featurelets = []
                for doc in c.flatten(1):
                    featurelets.append(set(doc.name.split(' ')))
                r = set.intersection(*featurelets)
                features.append(list(r))
                a = set.union(*featurelets) - set.intersection(*featurelets)
                alterTokens.append(list(a) + unique)
                unique = []
    return features, alterTokens

def prepare_description(txt):
    # Remove quotations and special characters and replace incorrect apostrophes 
    txt = filter_description(txt)

    # Tokenize, remove stop words
    txt = txt.decode('utf-8').strip()
    description = nltk.word_tokenize(txt)
    stopwords = nltk.corpus.stopwords.words('english')
    description = [i.encode("utf-8") for i in description if i not in stopwords]
    return description


def filter_description(txt):
    txt = txt.replace('"', '')
    txt = txt.replace('“', '')
    txt = txt.replace('”', '')
    txt = txt.replace("’", "'")
    txt = re.sub(r'(?:\@|https?\://)\S+', ' ', txt)
    txt = re.sub(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)', ' ', txt)
    txt = re.sub(r'[^\x00-\x7f]', ' ', txt)
    chars = [',','"','*',')','(','|','~','=',';',':','?','!','.','$','%','&','+','/','#',' - ','@','_']
    for char in chars:
        txt = txt.replace(char, ' ');
    return txt


def featurelet_extraction(description):
    # Tag text
    description = nltk.pos_tag(description)

    # Create Trigrams
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = nltk.collocations.TrigramCollocationFinder.from_words(description)

    # Filter non english characters
    finder.apply_word_filter(
        lambda w: w[1] in (
            '.', ',', ':', 'SYM', 'FW', 'UH'))

    # Filter by POS patterns:
    finder.apply_ngram_filter(lambda w1, w2, w3: (
        # Noun, Adj, __
        w1[1] not in ('NN', 'NNS') or
        w2[1] not in ('JJ', 'JJR', 'JJS') or
        w3[1] not in ('NN', 'NNS')
    ) and (
        # Verb/Determinate/Number, Adj, Noun
        w1[1] not in ('DT', 'CD', 'VB', 'VD', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ') or
        w2[1] not in ('JJ', 'JJR', 'JJS') or
        w3[1] not in ('NN', 'NNS')
    ) and (
        # Verb, Determinate/Noun, Noun
        w1[1] not in ('VB', 'VD', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP') or
        w2[1] not in ('DT', 'NN', 'NNS') or
        w3[1] not in ('NN', 'NNS')
    ) and (
        # Adj, Noun, Noun Plural
        w1[1] not in ('JJ', 'JJR', 'JJS') or
        w2[1] not in ('NN', 'NNS') or
        w3[1] != 'NNS'
    ) and (
        # Noun, Noun/verb, Noun
        w1[1] not in ('NN', 'NNS') or
        w2[1] not in ('NN', 'NNS', 'VB', 'VD', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ') or
        w3[1] not in ('NN', 'NNS')
    ) and (
        # Noun, Verb, Adjective
        w1[1] not in ('NN', 'NNS') or
        w2[1] not in ('VB', 'VD', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ') or
        w3[1] not in ('JJ', 'JJR', 'JJS')
    ) and (
        # Adjective/adverb, Verb, Noun/verb
        w1[1] not in ('RB', 'RBS', 'RBR', 'JJ', 'JJR', 'JJS') or
        w2[1] not in ('VB', 'VD', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ') or
        w3[1] not in ('NN', 'NNS', 'VB', 'VD', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')
    ) and (
        # Adverb, Adjective, Adjective
        w1[1] not in ('RB', 'RBS', 'RBR') or
        w2[1] not in ('JJ', 'JJR', 'JJS') or
        w3[1] not in ('JJ', 'JJR', 'JJS')
    ))

    # Filter meaningless end words
    finder.apply_ngram_filter(lambda w1, w2, w3: w3[1] in ('CC', 'IN', 'TO'))

    # Score and return featurlets
    scored = finder.score_ngrams(trigram_measures.pmi)
    list = []
    for trigram, score in scored:
        words = []
        for word, _ in trigram:
            words.append(word)
        list.append(words)
    return list


if __name__ == "__main__":
    extract()
