def is_valid_guess(guess: int) -> bool:
    assert guess is int, "Guess is not an integer, please input an integer"
    return guess > 0

def is_valid_word_in_dictionary(
    map_word_length_to_words: dict[int, list[str]], word: str
) -> bool:
    word = word.strip()
    if len(" ".split(word)) > 1:
        return False
    n = len(word)
    return n in map_word_length_to_words and word in map_word_length_to_words[n]

