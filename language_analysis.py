# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 18:11:09 2020
@author: nrdas
"""
#import statements
import json
import matplotlib.pyplot as plt
from langid.langid import LanguageIdentifier, model
import twokenize as tw


#Function to return list of world Tweets
def load_world_tweet_list():
    file2 = open("tweet_list.txt")
    tweet_list = []
    for line in file2:
        res = json.loads(line)
        tweet_list.append(res)
    #tweet_list = tweet_list[:15]
    return tweet_list

#Function to return list of USA Tweets
def load_us_tweet_list():
    file2 = open("us_tweets.txt")
    tweet_list = []
    for line in file2:
        res = json.loads(line)
        tweet_list.append(res)
    #tweet_list = tweet_list[:15]
    return tweet_list

#Function to analyze tweet languages
def analyze_twitter_languages(tweet_list):
    langdic = {}
    count = 0
    und_count = 0
    geo_count = 0
    coord_count = 0
    place_count = 0
    for tweet in tweet_list:
        if tweet['geo'] is not None:
            geo_count += 1
        if tweet['coordinates'] is not None:
            coord_count += 1
        if tweet['place'] is not None:
            place_count += 1
        language = tweet['lang']
        count += 1
        if language == 'und':
            und_count += 1
            continue
        if language in langdic:
            langdic[language] += 1
        else:
            langdic[language] = 1
    und_percent = int((10000*und_count/count)+0.5)/100
    print('There are ' + str(und_count) + ' unidentified tweets! That is ' + 
         str(und_percent) + '% of the Tweets captured! So ' + str(100-und_percent) + '% of tweets are LangID tagged!')
    print(str(len(langdic.keys())) + ' languages were tagged in the dataset generated')
    print(str(int((10000*geo_count/count)+0.5)/100) + '% were geo-tagged. ' + 
          str(int((10000*coord_count/count)+0.5)/100) + '% were coordinate tagged. ' +
          str(int((10000*place_count/count)+0.5)/100) + '% were place ID tagged.')
    return langdic

#Function to compare langid.py to Twitter lang tags
def compare_language_distribution(tweet_list):
    agreement_dic = {}
    disagreement_dic = {}
    guess_dic = {}
    pos_conf = []
    neg_conf = []
    clf = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    for tweet in tweet_list:
        language = tweet['lang']
        if language == 'und':
            continue   
        text = str(tweet['text'])
        #print(text)
        text = " ".join(map(str, tw.tokenizeRawTweetText(text)))
        #print(text)
        guess = clf.classify(text)
        if guess[0] in guess_dic:
            guess_dic[guess[0]] += 1
        else:
            guess_dic[guess[0]] = 1
        
        if guess[0] == language:
            pos_conf.append(guess[1])
            if language in agreement_dic:
                agreement_dic[language] += 1
            else:
                agreement_dic[language] = 1
        else:            
            neg_conf.append(guess[1])
            if language in disagreement_dic:
                disagreement_dic[language] += 1
            else:
                disagreement_dic[language] = 1
    print('The agreed inferences had a confidence of ' + str(sum(pos_conf)/len(pos_conf)) +
          '. The disagreed inferences had a confidence of ' + str(sum(neg_conf)/len(neg_conf)))
    return agreement_dic, disagreement_dic, guess_dic

print('Although Twitter only supports translated widget text of 34 languages, the annotation can have up to the 97 ISO 639-1 language tags.')
print('----------------- THE FOLLOWING ANALYSIS IS FOR THE WORLD STREAMED TWEETS -------------------')
world_tweet_list = load_world_tweet_list()
world_langdic = analyze_twitter_languages(world_tweet_list)
world_agreement_dic, world_disagreement_dic, world_guesses = compare_language_distribution(world_tweet_list)
print(str(len(world_guesses.keys())) + ' languages were detected in the dataset')

total = sum(world_disagreement_dic.values()) + sum(world_agreement_dic.values())
total_wrong = sum(world_disagreement_dic.values())
print("Precent different  out of the Tweets that were identified: " + str(int((10000*total_wrong/total)+0.5)/100) + '%')
#print("These are the disagreement frequencies: " + str(disagreement_dic))

plt.figure()
plt.bar(*zip(*world_disagreement_dic.items()))
plt.title('World Language Disagreement Distribution')
plt.show()


print('Here is the distribution of languages captured according to Twitter lang tags: ' + str(world_langdic))
tags = sum(world_langdic.values())
world_percents = {k: int((10000*v / tags)+0.5)/100 for k, v in world_langdic.items()}
print('Here are the corresponding percents: ' + str(world_percents))

plt.figure()
plt.pie(world_percents.values(), labels = world_percents.keys())
plt.title('World Composition of Twitter Language')
plt.show()

plt.figure()
plt.bar(*zip(*world_langdic.items()))
plt.title('World Twitter Language Distribution')
plt.show()


print('Here is the distribution of languages that were tagged in Twitter differently than in langid.py: ' + str(world_disagreement_dic))


print('----------------- THE FOLLOWING ANALYSIS IS FOR THE USA STREAMED TWEETS -------------------')
us_tweet_list = load_us_tweet_list()
us_langdic = analyze_twitter_languages(us_tweet_list)
us_agreement_dic, us_disagreement_dic, us_guesses = compare_language_distribution(us_tweet_list)
print(str(len(us_guesses.keys())) + ' languages were detected in the dataset')

total = sum(us_disagreement_dic.values()) + sum(us_agreement_dic.values())
total_wrong = sum(us_disagreement_dic.values())
print("Precent different out of the Tweets that were identified: " + str(int((10000*total_wrong/total)+0.5)/100) + '%')
#print("These are the disagreement frequencies: " + str(disagreement_dic))

plt.figure()
plt.bar(*zip(*us_disagreement_dic.items()))
plt.title('USA Language Disagreement Distribution')
plt.show()

print('Here is the distribution of languages captured according to Twitter lang tags: ' + str(us_langdic))
tags = sum(us_langdic.values())
us_percents = {k: int((10000*v / tags)+0.5)/100 for k, v in us_langdic.items()}
print('Here are the corresponding percents: ' + str(us_percents))

plt.figure()
plt.pie(us_percents.values(), labels = us_percents.keys())
plt.title('USA Composition of Twitter Language')
plt.show()

plt.figure()
plt.bar(*zip(*us_langdic.items()))
plt.title('USA Twitter Language Distribution')
plt.show()

print('Here is the distribution of languages that were tagged in Twitter differently than in langid.py: ' + str(us_disagreement_dic))








