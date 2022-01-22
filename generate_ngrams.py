

def generate_ngrams(tweets):
    big = ""
    for line in tweets:
        big += line + " TERMINATE "
    bigrams = []
    trigrams = []

    words_split = big.split(" ")
    for i in range(0, len(words_split) - 2):
        if words_split[i].lower() != 'terminate':
            bigrams.append([words_split[i], words_split[i + 1]])
            if words_split[i + 1].lower() != 'terminate':
                trigrams.append([words_split[i], words_split[i + 1], words_split[i + 2]])

    bigram_dict = {}
    for pair in bigrams:
        key = pair[0].lower() + " " + pair[1].lower()
        if len(pair[0]) <= 15 and len(pair[1]) <= 15:
            if "terminate" not in pair[0].lower() and "terminate" not in pair[1].lower():
                if key.lower() in bigram_dict:
                    bigram_dict[key.lower()] = bigram_dict[key.lower()] + 1
                else:
                    bigram_dict[key.lower()] = 1
    trigram_dict = {}
    for trip in trigrams:
        key = trip[0].lower() + " " + trip[1].lower() + " " + trip[2].lower()
        if len(trip[0]) <= 15 and len(trip[1]) <= 15:
            if "terminate" not in trip[0].lower():
                if key.lower() in trigram_dict:
                    trigram_dict[key.lower()] = trigram_dict[key.lower()] + 1
                else:
                    trigram_dict[key.lower()] = 1

    unigram_dict = {}
    for word in words_split:
        if word in unigram_dict:
            unigram_dict[word.lower()] = unigram_dict[word.lower()] + 1
        else:
            unigram_dict[word.lower()] = 1

    unigram_dict_cap = {}
    for word in words_split:
        if word in unigram_dict_cap:
            unigram_dict_cap[word] = unigram_dict_cap[word] + 1
        else:
            unigram_dict_cap[word] = 1

    first_words = []
    for tweet in tweets:
        word = tweet.split(" ")[0]
        if len(word) <= 15:
            first_words.append(word.lower())

    return bigram_dict, trigram_dict, first_words
