import os

import removeExesEtc
import generate
import generate_ngrams

def main():
    removeExesEtc.clean_csv()

    generate_ngrams.generate_ngrams()

    for i in range(10):
        print(generate.generate())


if __name__ == '__main__':
    main()
