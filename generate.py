import pickle
import random
import re


def generate():
    with open('uni.pickle', 'rb') as handle:
        unigram_dict = pickle.load(handle)

    with open('bi.pickle', 'rb') as handle:
        bigram_dict = pickle.load(handle)

    with open('first.pickle', 'rb') as handle:
        firstWords = pickle.load(handle)

    generated = False

    while not generated:
        written = ""
        written += firstWords[random.randint(0, len(firstWords))]
        previous = written

        while "terminate" not in written and "TERMINATE" not in written and "Terminate" not in written:
            nextWords = []
            for pair in bigram_dict:
                if pair.lower().split(" ")[0] == previous.lower():
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
            written += " " + next_word
            previous = next_word
            # print(len(nextWords))

        final = re.sub(" terminate| Terminate| TERMINATE", "", written)
        final = final.rstrip()
        final = re.sub(" go na ", " gonna ", final)
        final = final.capitalize()
        if final.count(" ") > 0 and len(final) <= 85:
            return final
            generated = True
