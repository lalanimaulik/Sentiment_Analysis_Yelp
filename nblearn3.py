import re
import sys
import string
import json
import random

map_reviews = {}
map_labels = {}
nbclass_count = {
	'deceptive':0,
	'truthful':0,
	'positive':0,
	'negative':0
}
stopWords = ['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now']
nbfeature_count = {}
nbProbability = {}
testing = True
def readTextFile():
	with open(sys.argv[1], 'r') as f:
	    reviews = f.readlines()
	if (testing):
		fp = open('test-text.txt', 'w')
		randomReviews = random.sample(reviews,200)
		# print (randomReviews)
		for i in randomReviews[:]:
			if i in reviews:
				randomReviews.remove(i)
				reviews.remove(i)
			fp.write("%s" % i)
	# print ("no of reviews = %s" % len(reviews))
	for review in reviews:
		r_split = review.split(' ',1)
		map_reviews[r_split[0]] = ' '.join(r_split[1:]).strip()  
	# print (map_reviews)

def readLabelFile():
	with open(sys.argv[2], 'r') as f:
	    labels = f.readlines()
	if (testing):
		fp = open('test-labels.txt','w')
	for label in labels:
		l_split = label.split(' ')
		if (testing):
			if (l_split[0] not in map_reviews):
				fp.write("%s" % label)
				continue
		map_labels[l_split[0]] = ' '.join(l_split[1:]).strip()  
	# print (map_labels)

def getWords(review_sentence):
	review_words = []
	for word in review_sentence.split():
		word = word.strip(string.punctuation).lower()
		if not word:
			continue
		if word in stopWords:
			# print ("word = ", word)
			continue
		# print (word)
		review_words.append(word)
	return review_words

def incrementWordCount(words, labels):
	for word in words:
		if not word:
			continue
		if (word not in nbfeature_count):
			nbfeature_count[word] = {}
			for key in nbclass_count:
				# print (key)
				nbfeature_count[word][key] = 0
		for label in labels.split(' '):
			nbfeature_count[word][label] = nbfeature_count[word][label] + 1
			nbclass_count[label] = nbclass_count[label] + 1;
			# print (nbfeature_count)
	# print (nbfeature_count)

def tokenize():
	for key,value in map_labels.items():
		# print (map_labels[key])
		if key in map_reviews:
			words = getWords(map_reviews[key])
			incrementWordCount(words, map_labels[key])
		else:
			print ("key = {0} not found".format(key))

def calculateFeatureProbability():
	total = len(nbfeature_count)
	for nbfeature in nbfeature_count:
		if nbfeature not in nbProbability:
			nbProbability[nbfeature] = {}
		for nbclass in nbclass_count:
			numerator = (nbfeature_count[nbfeature][nbclass] + 1)
			denominator = nbclass_count[nbclass] + total
			nbProbability[nbfeature][nbclass] = numerator / denominator  

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

readTextFile()
readLabelFile()
tokenize()
calculateFeatureProbability()
# print (nbfeature_count)
# print (nbProbability)
# print (nbclass_count)
newDict = {}
newDict['nbClassCount'] = nbclass_count
merged_dict = merge_two_dicts(nbProbability, newDict)
# print (json.dumps(merged_dict))
for word in merged_dict:
	print (word)
with open('nbmodel.txt', 'w') as fp:
    json.dump(merged_dict, fp)
# print(regex.sub(' ', strs))
# regex = re.compile('[%s]' % re.escape(string.punctuation))
# ' '.join(c for c in strs if c not in string.punctuation)
 # words = [x.strip(string.punctuation) for x in strs.split()]
