import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8,
                          'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
                          'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}

words_list_FILENAME = "words_scrabble.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    in_file = open(words_list_FILENAME, 'r')
    # words_list: list of strings
    words_list = []
    for line in in_file:
        words_list.append(line.strip().lower())
    print("  ", len(words_list), "words loaded.")
    return words_list


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word.
    """
    score = 0
    counter = 0
    for letter in word:
        score += SCRABBLE_LETTER_VALUES[letter]
        counter += 1
    if counter == n:
        return score*counter + 50
    elif counter <= n:
        return score*counter
    else:
        return "The word is too long"


def display_hand(hand):
    """
    Displays the letters currently in the hand.
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=" ")       # print all on the same line
    print()                             # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {}
    num_vowels = n // 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0, len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):
        x = CONSONANTS[random.randrange(0, len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand


def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    Returns the new hand, without those letters in it.
    Does not modify hand.
    """
    new_hand = dict(hand.items())
    
    for letter in word:
        new_hand[letter] = new_hand.get(letter, 0) - 1
        
    return new_hand


def is_valid_word(word, hand, words_list):
    """
    Returns True if word is in the words_list and is entirely
    composed of letters in the hand.
    """
    if word not in words_list:
        return False
    
    backup = updateHand(hand, word) 
    for letter in backup.keys():
        if backup[letter] < 0:
            return False
        
    return True


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    """
    length = 0  
    for i in hand.values():
        length += i
        
    return length


def play_hand(hand, words_list, n):
    """
    Allows the user to play the given hand      
    """
    total_score = 0

    while calculateHandlen(hand) != 0:
        displayHand(hand)
        word = input("enter the word \n")
        if word == '.':
            break            
        if not is_valid_word(word, hand, words_list):
            print("Invalid word, try again")
            print("\n")
        else:
            score = get_word_score(word, n)
            total_score += score
            print("you earned " + str(score) + " points, now your total score is " + str(total_score) + " points")
            print("\n")
            hand = update_hand(hand, word)

    print("your total score is " + str(total_score) + " points")


def play_game(words_list):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1    
    """
    while True:
        action = input("what do you want to do? n - new hand, r - replay hand, e - end game \n")
        if action == 'e':
            print("thanks for playing, goodbye")
            break
        elif action == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand, words_list, HAND_SIZE)
            print("round finished")
        elif action == 'r':
            try:
                play_hand(hand, words_list, HAND_SIZE)
                print("round finished")
            except UnboundLocalError:
                print("can't replay non-existent hand")
        else:
            print("invalid command")


if __name__ == '__main__':
    wordlist = load_words()
    play_game(wordlist)
