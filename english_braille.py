
from text_to_braille import *
from char_to_braille import *
from to_unicode import *
from helpers import *
import filecmp

from Braille_translator.text_to_braille import file_to_braille, new_filename

ENG_CAPITAL = '..\n..\n.o'
ENG_NUM_END = '..\n.o\n.o'

# You may want to define more global variables here

####################################################
# Here are two helper functions to help you get started

def two_letter_contractions(text):
    '''(str) -> str
    Process English text so that the two-letter contractions are changed
    to the appropriate French accented letter, so that when this is run
    through the French Braille translator we get English Braille.
    Provided to students. You should not edit it.

    >>> two_letter_contractions('chat')
    'âat'
    >>> two_letter_contractions('shed')
    'îë'
    >>> two_letter_contractions('shied')
    'îië'
    >>> two_letter_contractions('showed the neighbourhood where')
    'îœë ôe neiêbürhood ûïe'
    >>> two_letter_contractions('SHED')
    'ÎË'
    >>> two_letter_contractions('ShOwEd tHE NEIGHBOURHOOD Where') 
    'ÎŒË tHE NEIÊBÜRHOOD Ûïe'


    '''
    combos = ['ch', 'gh', 'sh', 'th', 'wh', 'ed', 'er', 'ou', 'ow']
    for i, c in enumerate(combos):
        text = text.replace(c, LETTERS[-1][i])
    for i, c in enumerate(combos):
        text = text.replace(c.upper(), LETTERS[-1][i].upper())
    for i, c in enumerate(combos):
        text = text.replace(c.capitalize(), LETTERS[-1][i].upper())

    return text


def whole_word_contractions(text):
    '''(str) -> str
    Process English text so that the full-word contractions are changed
    to the appropriate French accented letter, so that when this is run
    through the French Braille translator we get English Braille.

    If the full-word contraction appears within a word, 
    contract it. (e.g. 'and' in 'sand')

    Provided to students. You should not edit this function.

    >>> whole_word_contractions('with')
    'ù'
    >>> whole_word_contractions('for the cat with the purr and the meow')
    'é à cat ù à purr ç à meow'
    >>> whole_word_contractions('With')
    'Ù'
    >>> whole_word_contractions('WITH')
    'Ù'
    >>> whole_word_contractions('wiTH')
    'wiTH'
    >>> whole_word_contractions('FOR thE Cat WITh THE purr And The meow')
    'É thE Cat WITh À purr Ç À meow'
    >>> whole_word_contractions('aforewith parenthetical sand')
    'aéeù parenàtical sç'
    >>> whole_word_contractions('wither')
    'ùer'
    '''
    # putting 'with' first so wither becomes with-er not wi-the-r
    words = ['with', 'and', 'for', 'the']
    fr_equivs = ['ù', 'ç', 'é', 'à', ]
    # lower case
    for i, w in enumerate(words):
        text = text.replace(w, fr_equivs[i])
    for i, w in enumerate(words):
        text = text.replace(w.upper(), fr_equivs[i].upper())
    for i, w in enumerate(words):
        text = text.replace(w.capitalize(), fr_equivs[i].upper())
    return text



####################################################
# These two incomplete helper functions are to help you get started

def convert_contractions(text):
    '''(str) -> str
    Convert English text so that both whole-word contractions
    and two-letter contractions are changed to the appropriate
    French accented letter, so that when this is run
    through the French Braille translator we get English Braille.

    Refer to the docstrings for whole_word_contractions and 
    two_letter_contractions for more info.

    >>> convert_contractions('with')
    'ù'
    >>> convert_contractions('for the cat with the purr and the meow')
    'é à cat ù à purr ç à meœ'
    >>> convert_contractions('chat')
    'âat'
    >>> convert_contractions('wither')
    'ùï'
    >>> convert_contractions('aforewith parenthetical sand')
    'aéeù parenàtical sç'
    >>> convert_contractions('Showed The Neighbourhood Where')
    'Îœë À Neiêbürhood Ûïe'
    >>> convert_contractions('standardized')
    'stçardizë'
    '''
    #
    
    res = text.split(" ")
    for word in res: 
        word_new = two_letter_contractions(whole_word_contractions(word))
        text = text.replace(word, word_new)
    return text
    
def convert_quotes(text):
    '''(str) -> str
    Convert the straight quotation mark into open/close quotations.
    >>> convert_quotes('"Hello"')
    '“Hello”'
    >>> convert_quotes('"Hi" and "Hello"')
    '“Hi” and “Hello”'
    >>> convert_quotes('"')
    '“'
    >>> convert_quotes('"""')
    '“”“'
    >>> convert_quotes('" "o" "i" "')
    '“ ”o“ ”i“ ”'
    '''
    #
    
    res = ""
    i = 0
    for word in text:
        if word == '"':
            i += 1
            if i % 2 == 0:
                word = "”"
            else:
                word = "“"
        res += word

    return res


####################################################
# Put your own helper functions here!

def convert_parentheses(text):
    '''(str) -> str
    Convert open/close parentheses used in French Braille to parentheses used in English Braille.
    >>> convert_parentheses('(')
    '"'
    >>> convert_parentheses('aa aaaaaa(a')
    'aa aaaaaa"a'
    >>> convert_parentheses('ss(saw(2(')
    'ss"saw"2"'
    '''

    text = text.replace("(", '"')
    text = text.replace(")", '"')
    return text
    
def convert_q_mark(text):
    '''(str) -> str
    >>> convert_q_mark('www?')
    'www('
    '''

    text = text.replace("?", '(')
    return text

def convert_punctuation2(text):
    '''(str) -> str
    Convert parentheses, quotes and question mark in form of French Braille to English Braille.
    >>> convert_punctuation2('www?')
    'www('
    >>> convert_punctuation2('w wwww?')
    'w wwww('
    >>> convert_punctuation2('3456 12 ?& ? hi')
    '3456 12 (& ( hi'
    '''

    res = text.split(" ")
    for punctuation in res:
        punctuation_new = convert_q_mark(
                            (convert_parentheses(
                                convert_quotes(punctuation))))
        text = text.replace(punctuation, punctuation_new)
    return text 

def convert_num(text):
    '''
    >>> convert_num('2')
    '⠼⠃⠰'
    '''
    # res = ''
    # text_without_NUMBER = text.replace(ostring_to_unicode(NUMBER), "")
    # for i in range(len(text_without_NUMBER)):
    #     if is_digit(text_without_NUMBER[i]): # text_without_NUMBER is in form of unicode, cant be tested using is_digit
    #         if not is_digit(text_without_NUMBER[i+1]) and i < len(text_without_NUMBER)-1:
    #             res += ostring_to_unicode(ENG_NUM_END) + ostring_to_unicode('\n\n')
    #         if i == len(text_without_NUMBER)-1:
    #             res += ostring_to_unicode(ENG_NUM_END)
    #         if not is_digit(text_without_NUMBER[i-1]) and i >= 0:
    #             res # add in front of num
    # return res

    res = ""
    for i in range(len(text)):
        if is_digit(text[i]):
            if i-1 >=0 and not is_digit(text[i-1]):
                res += ostring_to_unicode(NUMBER)
            elif i == 0:
                res += ostring_to_unicode(NUMBER)

            res += ostring_to_unicode(convert_digit(text[i]))

            if i+1 < len(text) and not is_digit(text[i+1]):
                res += ostring_to_unicode(ENG_NUM_END)
            elif i == len(text)-1:
                res += ostring_to_unicode(ENG_NUM_END)

        else: res += text[i]
    return res

####################################################

def english_text_to_braille(text2):
    '''(str) -> str
    Convert text to English Braille. Text could contain new lines.

    This is a big problem, so think through how you will break it up
    into smaller parts and helper functions.
    Hints:
        - you'll want to call text_to_braille
        - you can alter the text that goes into text_to_braille
        - you can alter the text that comes out of text_to_braille
        - you shouldn't have to manually enter the Braille for 'and', 'ch', etc

    You are expected to write helper functions for this, and provide
    docstrings for them with comprehensive tests.

    >>> english_text_to_braille('202') # numbers
    '⠼⠃⠚⠃⠰'
    >>> english_text_to_braille('2') # single digit
    '⠼⠃⠰'
    >>> english_text_to_braille('COMP') # all caps
    '⠠⠠⠉⠕⠍⠏'
    >>> english_text_to_braille('COMP 202') # combining number + all caps
    '⠠⠠⠉⠕⠍⠏ ⠼⠃⠚⠃⠰'
    >>> english_text_to_braille('and')
    '⠯'
    >>> english_text_to_braille('and And AND aNd')
    '⠯ ⠠⠯ ⠠⠯ ⠁⠠⠝⠙'
    >>> english_text_to_braille('chat that the with')
    '⠡⠁⠞ ⠹⠁⠞ ⠷ ⠾'
    >>> english_text_to_braille('hi?')
    '⠓⠊⠦'
    >>> english_text_to_braille('(hi)')
    '⠶⠓⠊⠶'
    >>> english_text_to_braille('"hi"')
    '⠦⠓⠊⠴'
    >>> english_text_to_braille('COMP 202 AND COMP 250')
    '⠠⠠⠉⠕⠍⠏ ⠼⠃⠚⠃⠰ ⠠⠯ ⠠⠠⠉⠕⠍⠏ ⠼⠃⠑⠚⠰'
    >>> english_text_to_braille('For shapes with colour?')
    '⠠⠿ ⠩⠁⠏⠑⠎ ⠾ ⠉⠕⠇⠳⠗⠦'
    >>> english_text_to_braille('(Parenthetical)\\n\\n"Quotation"')
    '⠶⠠⠏⠁⠗⠑⠝⠷⠞⠊⠉⠁⠇⠶\\n\\n⠦⠠⠟⠥⠕⠞⠁⠞⠊⠕⠝⠴'
    >>> english_text_to_braille('standardized')
    '⠎⠞⠯⠁⠗⠙⠊⠵⠫'
    >>> english_text_to_braille('understand')
    '⠥⠝⠙⠻⠎⠞⠯'
    '''
    # You may want to put code after this comment. You can also delete this comment.

    # Here's a line we're giving you to get started: change text so the
    # contractions become the French accented letter that they correspond to

    paragraphs = text2.split('\n')
    total = ''

    for i, text in enumerate(paragraphs):
        text = convert_contractions(text)

        text = convert_punctuation2(text)

        text = convert_num(text)

        # You may want to put code after this comment. You can also delete this comment.

        # Run the text through the French Braille translator
        text = text_to_braille(text)

        # You may want to put code after this comment. You can also delete this comment.

        # Replace the French capital with the English capital
        text = text.replace(ostring_to_unicode(CAPITAL), ostring_to_unicode('..\n..\n.o'))

        text = text.replace('“', ostring_to_unicode('..\no.\noo'))

        text = text.replace('”', ostring_to_unicode('..\n.o\noo'))

        # You may want to put code after this comment. You can also delete this comment.

        total += text

        if i < len(paragraphs) - 1: # keep paragraphs separate but no extra \ns
            total += '\n'

    return total


def english_file_to_braille(fname):
    '''(str) -> NoneType
    Given English text in a file with name fname in folder tests/,
    convert it into English Braille in Unicode.
    Save the result to fname + "_eng_braille".
    Provided to students. You shouldn't edit this function.

    >>> english_file_to_braille('test4.txt')
    >>> file_diff('tests/test4_eng_braille.txt', 'tests/expected4.txt')
    True
    >>> english_file_to_braille('test5.txt')
    >>> file_diff('tests/test5_eng_braille.txt', 'tests/expected5.txt')
    True
    >>> english_file_to_braille('test6.txt')
    >>> file_diff('tests/test6_eng_braille.txt', 'tests/expected6.txt')
    True
    '''
    file_to_braille(fname, english_text_to_braille, "eng_braille")

if __name__ == '__main__':
    doctest.testmod()    # you may want to comment/uncomment along the way
    # and add tests down here
