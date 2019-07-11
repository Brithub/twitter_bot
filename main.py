import generate


def main():
    path = "cleaned_tweets.txt"
    with open(path, 'r') as file:
        text = file.read()
    tweets = text.split("\n")

    for i in range(15):
        print(generate.generate(tweets))


if __name__ == '__main__':
    main()
