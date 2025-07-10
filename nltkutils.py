import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
#from cltk.stem.lat import stem as latin_stem

stemmer = PorterStemmer()

latin_words = {
    "homo", "aeros", "auctor", "actor", "alumnus", "amicus", "amabilis", "amasius", "astutus", "argutus",
    "acer", "alacer", "armiger", "alacris", "agilis", "aemulus", "aequus", "aequaevus", "arrogans", "audax",
    "animosus", "animatus", "aelatus", "attollens", "avidus", "ambitiosus", "amarus", "adulter", "anceps",
    "atrox", "abstemius", "ablactatus", "aeger", "aerumnosus", "auspex", "astrosus", "aenormis", "abactor",
    "atratus", "advena", "alienigena", "accola", "agricola", "assecula", "assiduus", "apparator", "attentus",
    "attonitus", "allectus", "abactus", "abortivus", "adoptivus", "ambo", "alius", "aequimanus", "beatus",
    "bonus", "benignus", "beneficus", "benivolus", "blandus", "brutus", "balbus", "blaesus", "bucco",
    "biliosus", "baburrus", "biothanatus", "clarus", "celsus", "castus", "caeles", "caelebs", "caelicola",
    "continens", "clemens", "concors", "consolator", "consultus", "constans", "confidens", "cautus",
    "callidus", "cupidus", "clamosus", "calumniator", "calculator", "compilator", "contumax", "chromaticus",
    "contumeliosus", "contentiosus", "contemptibilis", "crudelis", "carnifex", "cruciarius", "collega",
    "coaetaneus", "complex", "consors", "celer", "confinalis", "colonus", "cognitor", "curator", "cliens",
    "captivus", "colomis", "comtus", "calamistratus", "corpulentus", "crassus", "comesor", "caupo",
    "canus", "caecus", "caducus", "confusus", "convulsus", "consumptus", "conciliatrix", "circumforanus",
    "dominus", "disertus", "doctus", "docilis", "discipulus", "dispensator", "dives", "decorus", "decens",
    "decibilis", "directus", "dilectus", "delibutus", "delicatus", "defessus", "debilis", "decolor",
    "desperatus", "degener", "decrepitus", "depretiatus", "dirus", "dehiscens", "despiciens", "dolosus",
    "dubius", "delator", "dilator"
}


def tokenize(sentence):
    
    return nltk.word_tokenize(sentence)


def stem(word):
    
    #if word in latin_words: 
        #return latin_stem(word.lower()) 
    #else:
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    
    
    sentence_words = [stem(word) for word in tokenized_sentence]
    
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag
