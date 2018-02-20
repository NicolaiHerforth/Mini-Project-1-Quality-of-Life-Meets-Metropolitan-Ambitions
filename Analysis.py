from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from afinn import Afinn
import csv



#Insert language
def get_language(caption):
#Splitting text into lowers case words
    words = wordpunct_tokenize(caption)
    words = [word.lower() for word in words]

    languages_dict = {}
    
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)
    
        languages_dict[language] = len(common_elements) # language "score"
        
    most_rated_language = str(max(languages_dict, key = languages_dict.get))
    if most_rated_language != 'english' and 'danish':
        most_rated_language = 'Unknown'
        
    return most_rated_language

def sentiment(sentence):
    """
    Requires afinn: "pip install afinn"
    Uses Danish made Afinn module to perform sentiment analysis on a word or sentence.
    Returns sentiment label: Positive, Neutral or Negative for given input.
    """
    afinn = Afinn(language = 'da')

    if afinn.score(sentence) > 0:
        return "Positive"
    elif afinn.score(sentence) == 0:
        return "Neutral"
    else:
        return "Negative"


def import_data(locations):
    id = 0
    d = {}
    for location in locations:
        dir_cap = "data/" + location + "/captions.txt"
        dir_full = "data/" + location + "/full_post.txt"
        dir_hash = "data/" + location + "/hashtags.txt"
        
        with open(dir_full, 'r') as a, open(dir_cap, 'r') as b, open(dir_hash, 'r') as c:
            for line_a, line_b, line_c in zip(a, b, c):
                #print(line_a, line_b, line_c)
                line_a = line_a.strip('\n').replace('#','')
                line_b = line_b.strip('\n')
                line_c = line_c.strip('\n')
                lang = get_language(line_a)
                senti = sentiment(line_a)
                d[id] = list()
                d[id].extend((line_a,line_b,line_c, lang, location, senti))
                id += 1

                    

    with open('dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        
        for key, value in d.items():
            writer.writerow([key,value[0],value[1],value[2],value[3],value[4],value[5]])

locations = ['valby']    
import_data(locations)
