# Hidden Markov Model for Parts of Speech Tagging

### Data
Corpus is in Catalan Language    
Traning Data: "catalan_corpus_train_tagged.txt"    
Raw Test Data: "catalan_corpus_dev_raw.txt"    
Tagger Test Data: "catalan_corpus_dev_tagged.txt"

### Hidden Markov Model 
Given observation as words, we need to find most likely tags of each word.
"Finding the most likely explanation for an observation sequence can be solved efficiently using the Viterbi algorithm."

Following the algorithm from Wiki - https://en.wikipedia.org/wiki/Viterbi_algorithm

### Programs
hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data.

> python hmmlearn.py /path/to/input

This will generate hmmmodel.txt
The format is as follows:    
countTransition  countEmission  countTags  possibleTagsForEachWord

The tagging program will be invoked in the following way:

> python hmmdecode.py /path/to/input

The program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt

