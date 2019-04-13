import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import csv


# import numpy


def read_text(path):
    inStream = open(path, encoding='utf-8-sig')
    lines = inStream.readlines()
    raw_string = ""
    for line in lines:
        raw_string = raw_string + line
    print(raw_string)
    return raw_string


def spilt_words(text):
    pattern = r"""(?x)                   # set flag to allow verbose regexps 
    	              (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A. 
    	              |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages 
    	              |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe 
    	              |\.\.\.                # ellipsis 
    	              |(?:[.,;"'?():-_`])    # special characters with meanings 
    	            """
    list = nltk.regexp_tokenize(text, pattern)
    print("spilt_words", len(list))
    return list


def stop_words(text_list):
    stopworddic = set(stopwords.words('english'))
    text_list = [i for i in text_list if i not in stopworddic]
    print("stop_words", len(text_list))
    return text_list


def words_prototype(text_list):
    wordnet_lemmatizer = WordNetLemmatizer()
    prototype_list = []
    for word in text_list:
        prototype_word = wordnet_lemmatizer.lemmatize(word)
        prototype_list.append(prototype_word)
    print("words_prototype", len(prototype_list))
    return prototype_list


def get_toefl_list():
    # with open("shanbay.csv", 'rb') as csvfile:
    #     reader = csv.reader(csvfile)
    #     toefl_list = [row[0] for row in reader]
    df = pd.read_csv("shanbay.csv")
    toefl_list = df["word"].tolist()
    print("get_toefl_list", len(toefl_list))
    return toefl_list


def map_toefl_words(toefl_list, text_list):
    intersection = [i for i in toefl_list if i in text_list]
    new_list = list(set(intersection))
    new_list.sort(key=intersection.index)
    print("map_toefl_words", len(intersection))
    return intersection


def get_meanings(list):
    df = pd.read_csv("shanbay.csv")
    df_filter = df.loc[(df["word"].isin(list))]
    df_filter.to_csv("result.csv")
    print(df_filter)


def print_list(list):
    file_handle = open('output.txt', mode='w')
    for word in list:
        file_handle.write(word + "\n")


def main():
    reading_passage_path = "reading.txt"
    text = read_text(reading_passage_path)
    list = spilt_words(text)
    prototype_list = words_prototype(list)
    after_clean_list = stop_words(prototype_list)
    map_list = map_toefl_words(get_toefl_list(), after_clean_list)
    get_meanings(map_list)
    # print_list(map_list)


if __name__ == '__main__':
    # nltk.download('stopwords')
    # nltk.download('wordnet')
    main()
