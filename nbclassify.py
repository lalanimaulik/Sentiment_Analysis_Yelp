import json
import string
import sys
with open('nbmodel.txt', 'r') as in_file:
	model = json.load(in_file)

output=open('nboutput.txt',"w")
test=open(sys.argv[1],"r")
testlist=test.readlines()
for line in range(len(testlist)):
	wordlist = testlist[line].split()
	deceptive=model['prior']['deceptive']
	truthful=model['prior']['truthful']
	positive=model['prior']['positive']
	negative=model['prior']['negative']
	id=wordlist[0]
	output.write(id)
	output.write(' ')
	wordlist.pop(0)
	for w in range(len(wordlist)):
		wordlist[w] = wordlist[w].translate(None, string.punctuation)
		if wordlist[w].lower() in model['deceptive']:
			deceptive= deceptive*float(model['deceptive'][wordlist[w].lower()])
			truthful=truthful*float(model['truthful'][wordlist[w].lower()])
			positive=positive*float(model['positive'][wordlist[w].lower()])
			negative=negative*float(model['negative'][wordlist[w].lower()])
	if deceptive>truthful:
		output.write('deceptive')
		output.write(' ')
	else:
		output.write('truthful')
		output.write(' ')
	if positive>negative:
		output.write('positive')
		output.write('\n')
	else:
		output.write('negative')
		output.write('\n')
