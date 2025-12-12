def sentence(sentence):

    no_of_characters = len(sentence)
    print("Number of characters in the sentence:", no_of_characters)

    no_of_words = len(sentence.split())
    print("Number of words in the sentence:", no_of_words)

    no_of_vowels = 0
    vowels = "aeiouAEIOU"
    for char in sentence:
        if char in vowels:
            no_of_vowels += 1
    print("Number of vowels in the sentence:", no_of_vowels)


