import random

WORDLIST_FILENAME = "words.txt"


def load_words():

    print("Loading word list from file...")
    in_file = open(WORDLIST_FILENAME, 'r')
    line = in_file.readline()
    words_list = line.split()
    print("  ", len(words_list), "words loaded.")
    return words_list


def choose_word(words_list):
    return random.choice(words_list)


def is_word_guessed(secret_word, letters_guessed):

    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):

    for letter in secret_word:
        if letter not in letters_guessed:
            print("_", end=" ")
        else:
            print(letter, end=" ")
    print("\n")


def get_available_letters(letters_guessed):
  
    available = 'abcdefghijklmnopqrstuvwxyz'
    print("available letters are ", end=": ")
    for letter in available:
        if letter not in letters_guessed:
            print(letter, end="")
    print("\n")


def hangman(secret_word):

    letters_guessed = []
    attempts = 8
    while not is_word_guessed(secret_word, letters_guessed):
        print("Attempts left: ", attempts)
        guess = input("Enter your guess letter \n")
        letters_guessed.append(guess)
        get_guessed_word(secret_word, letters_guessed)
        if is_word_guessed(secret_word, letters_guessed):
            print("You win!")
            break
        if letters_guessed[len(letters_guessed) - 1] not in secret_word:
            attempts -= 1
        if attempts == 0:
            print("You lose! The word was :", secret_word)
            break
        get_available_letters(letters_guessed)


wordlist = load_words()
the_word = choose_word(wordlist)
print("your word contains {} letters".format(len(the_word)))
hangman(the_word)
