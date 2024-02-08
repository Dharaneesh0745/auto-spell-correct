from flask import Flask, request, render_template
import re
import pandas as pd
from pattern.en import lexeme

print(dir(re))

app = Flask(__name__)

final = "C:/Users/dhara.LAPTOP-VAF0SV4G/Downloads/final.txt"

with open(final, 'r', encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    main_set = set(re.findall(r'\w+', file_name_data))

def counting_words(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def prob_cal(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs

def DeleteLetter(word):
    delete_list = []
    for i in range(len(word)):
        delete_list.append(word[:i] + word[i+1:])
    return delete_list

def colab_1(word, allow_switches=True):
    colab_1 = set()
    colab_1.update(DeleteLetter(word))
    if allow_switches:
        colab_1.update(Switch_(word))
    colab_1.update(Replace_(word))
    colab_1.update(insert_(word))
    return colab_1

def Replace_(word):
    replace_list = []
    for i in range(len(word)):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            replace_list.append(word[:i] + char + word[i+1:])
    return replace_list

def insert_(word):
    insert_list = []
    for i in range(len(word) + 1):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            insert_list.append(word[:i] + char + word[i:])
    return insert_list

def Switch_(word):
    split_list = []
    switch_l = []
    for i in range(len(word)):
        split_list.append((word[:i], word[i:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_list if len(b) >= 2]
    return switch_l

def get_corrections(word, probs, vocab, n=2):
    suggested_word = []
    best_suggestion = []
    suggested_word = list(
        (word in vocab and word) or colab_1(word).intersection(vocab)
        or colab_2(word).intersection(vocab))
    best_suggestion = [[s, probs[s]] for s in list(reversed(suggested_word))]
    return best_suggestion[:n]

def spell_check(input_word):
    word_count = counting_words(main_set)
    probs = prob_cal(word_count)
    return get_corrections(input_word, probs, main_set, 3)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/spell_check', methods=['POST'])
def spell_check_route():
    input_word = request.form['input_word']
    corrections = spell_check(input_word)
    return render_template('index.html', input_word=input_word, corrections=corrections)

if __name__ == '__main__':
    app.run(debug=True)
