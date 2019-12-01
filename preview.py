import generate
import glob

def main():
    files = glob.glob("databases/*.txt")

    tweets = []

    for user in files:
        with open(user, 'r', encoding="utf-8") as file:
            text = file.read()
        user_tweets = text.split("\n")
        tweets.append(user_tweets)

    for i in range(15):
        print(generate.generate(tweets))


if __name__ == '__main__':
    main()
