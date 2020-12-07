import string

lstr = string.ascii_lowercase[:]
ustr = string.ascii_uppercase[:]
WORDLIST_FILENAME = 'words.txt'


def load_words(file_name):
    """
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    in_file = open(file_name, 'r')
    line = in_file.readline()
    word_list = line.split()
    in_file.close()
    return word_list


def is_word(word_list, word):
    """
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


class Message(object):
    def __init__(self, text):
        """
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        """
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        """
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        """
        return self.message_text

    def get_valid_words(self):
        """
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        """
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        """
        Creates a dictionary that can be used to apply a cipher to a letter.
         Returns: a dictionary mapping 
        """
        shift_dict = {}
        for letter in lstr:
            if (ord(letter) + shift) in range(ord('a'), ord('z') + 1):
                shifted_letter = chr(ord(letter) + shift)
                shift_dict[letter] = shifted_letter
            else:
                shifted_letter = chr(ord(letter) + shift - (ord('z') - ord('a') + 1))
                shift_dict[letter] = shifted_letter

        for letter in ustr:
            if (ord(letter) + shift) in range(ord('A'), ord('Z') + 1):
                shifted_letter = chr(ord(letter) + shift)
                shift_dict[letter] = shifted_letter
            else:
                shifted_letter = chr(ord(letter) + shift - (ord('Z') - ord('A') + 1))
                shift_dict[letter] = shifted_letter
        return shift_dict

    def apply_shift(self, shift):
        """
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string.
        """
        new_word = ''
        for letter in self.message_text:
            dictionary = self.build_shift_dict(shift)
            if letter in dictionary.keys():
                new_letter = dictionary[letter]
                new_word += new_letter
            else:
                new_word += letter
        return new_word


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        """
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        """
        Message.__init__(self, text)
        self.shift = shift
        self.encrypting_dict = {}
        self.message_text_encrypted = ""

    def get_shift(self):
        """
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        """
        return self.shift

    def get_encrypting_dict(self):
        """
        Used to safely access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        """
        self.encrypting_dict = self.build_shift_dict(self.shift)
        return dict(self.encrypting_dict.items())

    def get_message_text_encrypted(self):
        """
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        """
        self.message_text_encrypted = self.apply_shift(self.shift)
        return self.message_text_encrypted

    def change_shift(self, shift):
        """
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        """
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        """
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        Message.__init__(self, text)

    def decrypt_message(self):
        """
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        """
        max_correct_number = 0
        for i in range(1, 27):
            decryption_attempt = self.apply_shift(i)
            correct_word_number = 0
            for a_word in decryption_attempt.split(" "):
                if is_word(self.valid_words, a_word):
                    correct_word_number += 1
                if correct_word_number > max_correct_number:
                    max_correct_number = correct_word_number
                    actual_key = i
                    actual_text = decryption_attempt
        return (actual_key, actual_text)


plaintext = PlaintextMessage('hello', 2)
print('Coded message for {} is : {}'.format(plaintext.get_message_text(),
                                            plaintext.get_message_text_encrypted()))

ciphertext = CiphertextMessage("L hdw d orw ri fruq, yhub wdvwb")
print('Cipher is {}; actual message was : {}'.format(ciphertext.get_message_text(),
                                                     ciphertext.decrypt_message()[1]))

decrypted_story = CiphertextMessage(get_story_string())
print('The story was : \n {}'.format(decrypted_story.decrypt_message()[1]))
