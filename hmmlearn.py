import json
import io
from collections import defaultdict
import sys
# Training in this file


# This file generates the hmmmodel.txt file


# let us assume first tag is <s> and end tag is </s>
file_path = sys.argv[1]
print file_path
lines = [line.rstrip('\n') for line in open(file_path)]
# print(len(lines))
emission = defaultdict(int)

transition = defaultdict(int)

context = defaultdict(int)

possible_tags_of_words = dict()




# assuming first tag is <s> even if its not
# P_Transition(LRB|NN) = c(NN LRB)/c(NN)
# P_Emission(language|NN) = c(NN -> language)/c(NN)

for line in lines:
    #print(line)

    # line is splitted with " ", so splitted line will is a list of word/tag
    splitted_line = line.split(" ")

    # print(splitted_line)
    previous = '<s>'

    context[previous] += 1
    for wordAndTag in splitted_line:
        len_wordAndTag = len(wordAndTag)
        word = wordAndTag[:len_wordAndTag-3]
        tag = wordAndTag[-2:]

        if word in possible_tags_of_words:
            possible_tags_of_words[word].add(tag)
        else:
            possible_tags_of_words[word] = set()
            possible_tags_of_words[word].add(tag)

        key_for_transition = previous+' '+tag
        key_for_emission = tag+' '+word

        context[tag] += 1

        emission[key_for_emission] += 1

        transition[key_for_transition] += 1

        previous = tag

    transition[previous+' </s>'] += 1

count_transition = len(transition)
count_emission = len(emission)
count_context = len(context)
count_words = len(possible_tags_of_words)
file_model = open('hmmmodel.txt','wb')

file_model.write(str(count_transition)+' '+str(count_emission)+" "+str(count_context)+" "+str(count_words)+'\n')


for key, value in transition.iteritems():
    file_model.write(key+' '+str(value)+'\n')




for key, value in emission.iteritems():
    file_model.write(key+' '+str(value)+'\n')



for key, value in context.iteritems():
    file_model.write(key+' '+str(value)+'\n')

for key, value in possible_tags_of_words.iteritems():
    file_model.write(key+' ')
    for all_tags in value:
        file_model.write(all_tags+' ')
    file_model.write('\n')
