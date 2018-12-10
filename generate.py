import pickle
import random
import re


def generate_next_word(written,bigram_dict,trigram_dict):

    #use bigrams for the second word
    if written.count(" ") < 2 or random.randint(0,100) > 50:
        return generate_from_bigrams(written,bigram_dict)
    else:
        return generate_from_trigrams(written,trigram_dict,bigram_dict)


def generate_from_bigrams(prev,bigram_dict):
    last_word = prev.split(" ")[-1]
    nextWords = []
    for pair in bigram_dict:
        if pair.lower().split(" ")[0] == last_word.lower():
            nextWords.append([pair, bigram_dict[pair]])
    if len(nextWords) == 1:
        next_word = nextWords[0][0].split(" ")[1]
    elif len(nextWords) == 0:
        next_word = "terminate"
    else:
        total = 0
        for pair in nextWords:
            total += pair[1]
        chosen = random.randint(1, total) - 1
        searching = 0
        index = 0
        temp_word = ""
        while searching < chosen:
            temp_word = nextWords[index][0].split(" ")[1]
            searching += nextWords[index][1]
            index += 1
        next_word = temp_word
    return next_word


def generate_from_trigrams(prev,trigram_dict,bigram_dict):
    if len(prev.split(" ")) < 2:
        return "error"

    old = prev.split(" ")[-1]
    older = prev.split(" ")[-2]

    nextWords = []
    for trip in trigram_dict:
        if trip.lower().split(" ")[0]+" "+trip.lower().split(" ")[1] == older.lower()+" "+old.lower():
            nextWords.append([trip, trigram_dict[trip]])
    if len(nextWords) == 1:
        next_word = nextWords[0][0].split(" ")[2]
    elif len(nextWords) == 0:
        next_word = generate_from_bigrams(prev,bigram_dict)
    else:
        total = 0
        for pair in nextWords:
            total += pair[1]
        chosen = random.randint(1, total) - 1
        searching = 0
        index = 0
        temp_word = ""
        while searching < chosen:
            temp_word = nextWords[index][0].split(" ")[2]
            searching += nextWords[index][1]
            index += 1
        next_word = temp_word
    return next_word


def generate():
    with open('uni.pickle', 'rb') as handle:
        unigram_dict = pickle.load(handle)

    with open('bi.pickle', 'rb') as handle:
        bigram_dict = pickle.load(handle)

    with open('first.pickle', 'rb') as handle:
        firstWords = pickle.load(handle)

    with open('tri.pickle', 'rb') as handle:
        trigram_dict = pickle.load(handle)

    generated = False

    while True:
        written = ""
        written += firstWords[random.randint(0, len(firstWords)-1)]

        while "terminate" not in written and "TERMINATE" not in written and "Terminate" not in written:
            generated = generate_next_word(written,bigram_dict,trigram_dict)
            written += " " + generated


        final = re.sub(" terminate| Terminate| TERMINATE", "", written)
        final = final.rstrip()
        final = re.sub(" gon na ", " gonna ", final)
        final = re.sub(" got ta ", " gotta ", final)
        final = re.sub(" wan na ", " wanna ", final)
        final = re.sub(" n't ", "n't ", final)
        final = re.sub(" 've ", "'ve ", final)
        final = re.sub(" 're ", "'re ", final)
        final = re.sub(" im ", " I'm ", final)
        final = re.sub(" i ", " I ", final)
        final = final.capitalize()
        if final.count(" ") > 1 and len(final) <= 85:
            return final