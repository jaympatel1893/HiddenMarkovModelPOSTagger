from __future__ import division
from collections import defaultdict
import sys
import time
def viterbi(observation):
    # print(observation)
    len_observtion = len(observation)
    V = [defaultdict(int)]
    backpointer = [defaultdict(int)]
    # print(states)

    for i in states:
        key_for_emission = i+' '+observation[0]
        if observation[0] in possible_tags_of_words:
            V[0][i] = ((transition['<s> '+i]+1)/(context['<s>']+len(states)))*(emission[key_for_emission]/context[i])
        else:
            V[0][i] = ((transition['<s> '+i]+1)/(context['<s>']+len(states)))
        backpointer[0][i] = '<s>'
    # print V[0]
    for t in range(1, len(observation)):
        V.append(defaultdict(int))
        backpointer.append(defaultdict(int))
        if observation[t] in possible_tags_of_words:
            # if the word is seen in training data
            # print (observation[t]+" is seen")
            all_tags_for_this_word = possible_tags_of_words[observation[t]]
            for y in all_tags_for_this_word:
                key_for_emission = y+' '+observation[t]
                max_value = -1
                max_previous_state = ''
                for previous_state in states:
                    transition_pro = (transition[previous_state+' '+y]+1)/(context[previous_state]+len(states))
                    emission_pro = (emission[key_for_emission])/(context[y])
                    # prob = max(V[t - 1][y0]*(transition[y0+' '+y]/context[y0])*(emission[key_for_emission]/context[y]) for y0 in states)
                    if V[t-1][previous_state] == 0:
                        continue
                    else:
                        temp_value = V[t-1][previous_state]*transition_pro*emission_pro
                        if max_value <= temp_value:
                            max_value = temp_value
                            max_previous_state = previous_state

                backpointer[t][y] = max_previous_state
                # if max_value==(-sys.maxint-1):
                #     V[t][y] = 0
                # else:
                V[t][y] = max_value
        else:
            # The word is not found in the training corpus
            # print (observation[t]+" is not seen")
            for y in states:
                max_value = - 1
                max_previous_state = ''
                for previous_state in states:
                    transition_pro = (transition[previous_state+' '+y]+1)/(context[previous_state]+len(states))
                    if V[t-1][previous_state] == 0:
                        continue
                    else:
                        temp_value = V[t-1][previous_state]*transition_pro

                        if max_value <= temp_value:
                            max_value = temp_value
                            max_previous_state = previous_state

                backpointer[t][y] = max_previous_state
                V[t][y] = max_value

    # print(V[-1])
    # find max in last stage
    max_value = -1
    max_state_last = ''
    for key, value in V[-1].iteritems():
        if value>=max_value:
            max_value = value
            max_state_last = key

    # print("bc")



    my_tags = []

    current_state = max_state_last


    back_counter = len_observtion-1
    while back_counter!=-1 or current_state!='<s>':

        my_tags.insert(0, current_state)
        # print my_tags
        # print ("Rascal"+str(current_state))

        current_state = backpointer[back_counter][current_state]
        if current_state=='':
            for key, val in backpointer[back_counter-1].iteritems():
                current_state = (backpointer[back_counter-1][key])
                my_tags.insert(0,key)
                back_counter-=1
                break
        back_counter -= 1
        # print(current_state),
        # print(back_counter)
    return my_tags



import sys
file_path = sys.argv[1]
lines = [line.rstrip('\n') for line in open('hmmmodel.txt')]
# print(len(lines))

len_transition, len_emission, len_context, len_words = lines[0].split(" ")

len_transition = int(len_transition)

len_emission = int(len_emission)

len_context = int(len_context)

len_words = int(len_words)

transition = defaultdict(int)

emission = defaultdict(int)

context = defaultdict(int)

states = set()

possible_tags_of_words = dict()


lines.pop(0)

for i in range(0,len_transition):
    splitted_line = lines[0].split(" ")
    transition[splitted_line[0]+' '+splitted_line[1]] = int(splitted_line[2])
    lines.pop(0)

for i in range(0,len_emission):
    splitted_line = lines[0].split(" ")
    emission[splitted_line[0]+' '+splitted_line[1]] = int(splitted_line[2])
    lines.pop(0)

for i in range(0,len_context):
    splitted_line = lines[0].split(" ")
    context[splitted_line[0]] = int(splitted_line[1])
    lines.pop(0)

for i in range(0,len_words):
    splitted_line = lines[0].strip().split(" ")
    word = splitted_line[0]
    possible_tags_of_words[word] = set()
    for j in range(1,len(splitted_line)):
        possible_tags_of_words[word].add(splitted_line[j])
    lines.pop(0)

for key, value in context.iteritems():
    states.add(key)

# print possible_tags_of_words[0]
# print(len(lines))


# Starting Viterbi

input_lines = []
for line in open(file_path):
    input_lines.append(line.rstrip('\n'))

file_output = open('hmmoutput.txt','wb')

start = time.time()
for line in input_lines:
    #split every line with a " "
    #this will be our observation
    observation = [word for word in line.split(' ')]
    try:
        tags_returned = viterbi(observation)

    # print tags_returned
        output_line = ""
        for i in range(0,len(observation)):
            output_line+=observation[i]+'/'+tags_returned[i]+" "

        file_output.write(output_line+'\n')
    except:

        tags_returned = []
        tag = ""
        for key, value in possible_tags_of_words.iteritems():
            tag = key
            break
        for i in range(0, len(observation)):
            tags_returned.append(tag)
        output_line = ""
        for i in range(0,len(observation)):
            output_line+=observation[i]+'/'+tags_returned[i]+" "

        file_output.write(output_line+'\n')
        pass

end = time.time()

print (end-start)