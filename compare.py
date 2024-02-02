from Levenshtein import distance

def find_mistakes(sentence1, sentence2):
    mistakes = []
    #marked_mistakes = []

    # Bepaal de fonemen voor de zinnen
    phonemes1 = get_phonemes(sentence1)
    phonemes2 = get_phonemes(sentence2)

    # Zoek naar verschillen tussen de fonemen
    distance_levenshtein = distance(phonemes1, phonemes2)
    if distance_levenshtein > 0:  # Change from > 1 to > 0
        # Voeg de fouten toe aan de lijst
        mistakes.extend(find_missing_phonemes(sentence1, sentence2))
        # Markeer de fout in de uitspraak
        #marked_mistakes = mark_mistakes(sentence2, mistakes)

    return mistakes #, marked_mistakes

def get_phonemes(sentence):
    # Dit is een eenvoudige mapping van letters naar fonemen voor het Nederlands.
    phoneme_dict = {
        'a': 'ah',
        'b': 'bee',
        'c': 'see',
        'd': 'dee',
        'e': 'ee',
        'f': 'eff',
        'g': 'gee',
        'h': 'aych',
        'i': 'eye',
        'j': 'jay',
        'k': 'kay',
        'l': 'ell',
        'm': 'em',
        'n': 'en',
        'o': 'oh',
        'p': 'pee',
        'q': 'kew',
        'r': 'ar',
        's': 'ess',
        't': 'tee',
        'u': 'you',
        'v': 'vee',
        'w': 'double you',
        'x': 'ecks',
        'y': 'why',
        'z': 'zee'
    }

    # Converteer de letters van de zin naar fonemen
    phonemes = [phoneme_dict.get(letter.lower(), letter) for letter in sentence]

    return phonemes

def find_missing_phonemes(sentence1, sentence2):
    missing_phonemes = []

    words1 = sentence1.split()
    words2 = sentence2.split()

    for word1, word2 in zip(words1, words2):
        phonemes1 = get_phonemes(word1)
        phonemes2 = get_phonemes(word2)

        if phonemes1 != phonemes2:
            missing_phonemes.extend(find_missing_phonemes_in_word(phonemes1, phonemes2))

    return missing_phonemes

def find_missing_phonemes_in_word(phonemes1, phonemes2):
    return list(set(phonemes1) - set(phonemes2))