from string import punctuation
from collections import Counter
import io
import time
import re
import math
from operator import itemgetter

start = time.time()

def unique_words(sentence):
    		return set(sentence.translate(None, punctuation).lower().split())

stopwords=set(line.strip().translate(None, punctuation).lower() 	for line in open('MYSTWORD.TXT'))

#for w in stopwords:
#	print w
 
#------The next code splits the document into sentences 
#               and returns it as a set of sentences--------- 

with open ("data.txt", "r") as myfile:
    data=myfile.read().replace('\n', ' ')
sentences = re.split("[\.\?][ ][ ]*", data)
#print data+"\n"
#print sentences


#------------------------------------------------------------

#this part removes stopwords and remakes the sentences----

new_sentences = []
for s in sentences:
	#one_sentence = unique_words(s)
	s = s.lower()
	one_sentence = re.sub("[^\w]", " ",  s).split()
	filtered_sentence = [w for w in one_sentence if not w in stopwords]	
	stringbuffer=" ".join(str(n) for n in filtered_sentence)
	new_sentences.append(stringbuffer)



#print new_sentences
print "\n"
print "Number of sentences: "+ str(len(new_sentences))
print "\n"


#---------------------------------------------------------------
# This section finds all the unique words in the document and returns their set

completedocsent = " ".join(str(q) for q in new_sentences)
#print completedocsent
 
all_unique_words  = unique_words(completedocsent)
num_unique = len(all_unique_words)
print "Total unique words " + str(len(all_unique_words))
#print all_unique_words


#---------------------------------------------------------------
# Calculates df for all terms
# df = how many sentences the term is present in, 
# Returns 'df' as a set containing dfs of all unique words

df = set()

for w in all_unique_words:
	k=0
	for s in new_sentences:
		words = s.split()
		if w in words:
			k += 1
			df.add((w, k))
#print "Document frequency of each unique term..\n"
'''print df'''
print "\n"

#-----------------------------------------------------------------
# Now we calculate tf for all terms

tf = set()
k=1
for s in new_sentences:
	terms = s.split()
	for t in terms:
		tf.add((t, terms.count(t), k))
	k += 1
tf = sorted(tf, key = itemgetter(2))
# 'k' is the sentence number 
#print "Term frequencies... \n"
'''for tup in tf:
	print tup'''
#print "\n"

#-----------------------------------------------------------------
# Now, we calculate the weight matrix

wt_mat = set()
for w in all_unique_words:
	for d in df:
		if d[0] == w:
			tempdf = d[1]
	for t in tf:
		if t[0] == w:
			temptf = d[1]
	wt_mat.add((w, temptf * math.log(num_unique / tempdf)))

#print wt_mat
#print num_unique

#-------------------------------------------------------------------
# this section will turn each sentence into a vector of all unique words
# and return a matrix 'final' with wt-vectors of all sentences
 
final = []
vector = []
for s in new_sentences:
	vector = []
	tokens = s.split()
	for w in all_unique_words:
		if w in tokens:
			for wt in wt_mat:	
			 	if wt[0] == w:
					vector.append(float(wt[1]))
		else:
			vector.append(0.0)
	final.append(vector)
'''for kitty in final:
	print kitty
	print "\n"
print len(final)'''
	
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Relevance Score Calculation

def product(vector):
	product = 0
	for vector in final:
		for t in vector:
			product += t*t
	return product


newlist = []
relev = []
print "The following are the relevance scores of the sentences: \n"
for vect1 in final:
	nsum=0
	for vect2 in final:
		i=0
		if vect1 != vect2:
			a = 0.0
			d = math.sqrt(product(vect1)*product(vect2))
			for i in range(0,40):
				a += vect1[i]*vect2[i]
			nsum += a/d
				
	#newlist.append(nsum)
	relev.append(nsum)
	print nsum
print "\n"
		
#--------------------------------------------------------------------------------	

# sorting relev in increasing order

included = []								# included is a list of concluded index
sents = len(relev)							# numbers of summarized sentences
index_sent = sorted(range(len(relev)), key = lambda i:relev[i])
f = 0
for f in range(sents-6, sents):
	included.append(index_sent[f])


#-------------------------------------------------------------------------------
# The Summarized sentences are outputted

print "Summarized document with the compression ratio of 6 sentences :: "
print "\n"
for h in range(0,6):
	print str(h+1)+ ".) " + sentences[included[h]] + ".\n"

stop = time.time()

print "Processing time : "+ str(stop-start) +" seconds" + "\n"
#--------------------------------------------------------------------------------





