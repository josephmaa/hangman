from collections import defaultdict


def parse_dictionary(dictionary_file: str = "") -> dict[int, str]:
    word_length_to_words = defaultdict(list)
    with open(dictionary_file) as f:
        for line in f.readlines():
            word = line.strip()
            n = len(word)
            word_length_to_words[n].append(word)
    return word_length_to_words
