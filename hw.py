import nltk
from nltk.corpus import stopwords
from nltk.corpus import senseval as se
from nltk. corpus import wordnet as wn
from nltk.stem import *

#   Creating stemmer
stemmer = SnowballStemmer("english")

#   Removing standart stopwords and your customed list
def remove_nltk_stop_words(tokens):
    new_list = [i for i in tokens if i not in my_stop_list]
    return new_list
def remove_stop_words(tokens):
    new_list=[i for i in tokens if i not in nltk_stop_list]
    return new_list

#    Basically there should be just "hard.pos" but in my computer it requires the absolute path
sv_instances = se.instances("/Users/ilyas/nltk_data/corpora/senseval/hard.pos")
#   A stop-words list with base stop symbols
my_stop_list = [',','.','``',"''",')','(','!','?',':',';','$','>','<','[',']',"'","''","--",'"']
nltk_stop_list = set(stopwords.words('english'))
#   I found this vocabulary in the web. Basically it matches tags between Wordnet and senseval
SV_SENSE_MAP = {
    "HARD1": ["difficult.a.01"],    # not easy, requiring great physical or mental
    "HARD2": ["hard.a.02",          # dispassionate
              "difficult.a.01"],
    "HARD3": ["hard.a.03"],         # resisting weight or pressure
    "interest_1": ["interest.n.01"], # readiness to give attention
    "interest_2": ["interest.n.03"], # quality of causing attention to be given to
    "interest_3": ["pastime.n.01"],  # activity, etc. that one gives attention to
    "interest_4": ["sake.n.01"],     # advantage, advancement or favor
    "interest_5": ["interest.n.05"], # a share in a company or business
    "interest_6": ["interest.n.04"], # money paid for the use of money
    "cord": ["line.n.18"],          # something (as a cord or rope) that is long and thin and flexible
    "formation": ["line.n.01","line.n.03"], # a formation of people or things one beside another
    "text": ["line.n.05"],                 # text consisting of a row of words written across a page or computer screen
    "phone": ["telephone_line.n.02"],   # a telephone connection
    "product": ["line.n.22"],       # a particular kind of product or merchandise
    "division": ["line.n.29"],      # a conceptual separation or distinction
    "SERVE12": ["serve.v.02"],       # do duty or hold offices; serve in a specific function
    "SERVE10": ["serve.v.06"], # provide (usually but not necessarily food)
    "SERVE2": ["serve.v.01"],       # serve a purpose, role, or function
    "SERVE6": ["service.v.01"]      # be used by; as of a utility
}

#   Reading the subset of 300 examples
ex = sv_instances[220:520] + sv_instances[3500:3550] + sv_instances[4100:4150]    #subset of 300 examples
#   Setting initial values for the precision calculation
occ_num=0
total_num=0
#   First cycle for each sentence in har.pos
for sent in ex:
#   Get curr sense of word
  sense = sent.senses[0]
#   Get current word, it comes in form hard-a where hard - word, a - part of speech, so we need to split it
  cur_word = str(sent.word)
  word_pos_list = cur_word.split("-")
  cur_word = word_pos_list[0]
  sv_pos = word_pos_list[1]
#   Get all lemmas of word
  lemma_list = wn.lemmas(wn.morphy(cur_word), wn.ADJ)
#   Get all words from the context, removing stop words and making a list from it
  context_tokens = [a[0] for a in sent.context]
  #context_tokens = " ".join(a[0] for a in sent.context)
  #context_tokens = nltk.word_tokenize(context_tokens)
  context_tokens = [t.lower() for t in context_tokens]
  context_tokens = remove_stop_words(context_tokens)
  context_tokens = remove_nltk_stop_words(context_tokens)
  context_tokens = [stemmer.stem(w) for w in context_tokens]
#   Setting values for Simp Lesk algo
  best_sense=""
  max_overlap=0
#   Beginning of the Simp Lesk algo
  for lemma in lemma_list:
      syn = lemma.synset()
      #print(syn.name())
#   Get tokens from the definition of the word and filter them
      def_tokens = nltk.word_tokenize(syn.definition())
      def_tokens = [t.lower() for t in def_tokens]
      def_tokens = remove_stop_words(def_tokens)
      def_tokens = remove_nltk_stop_words(def_tokens)
      def_tokens = [stemmer.stem(w) for w in def_tokens]
#   Get tokens from the examples of the word and filter them
      ex_tokens = " ".join(syn.examples())
      ex_tokens = nltk.word_tokenize(ex_tokens)
      ex_tokens = [t.lower() for t in ex_tokens]
      ex_tokens = remove_stop_words(ex_tokens)
      ex_tokens = remove_nltk_stop_words(ex_tokens)
      ex_tokens = [stemmer.stem(w) for w in ex_tokens]
#   Form the signature as union of def and examples
      signature = list(set().union(def_tokens,ex_tokens))
#   Find the intersection which is actually the overlap
      inter_list = list(set(signature) & set(context_tokens))
#   Just remove # to see the output
      #print("Signature: ", signature)
      #print("Context tokens: ", context_tokens)
      #print("Intersec: ", inter_list)
      if max_overlap<len(inter_list):
          max_overlap = len(inter_list)
          best_sense = lemma
#   Matching tags and calc precision
  if str(best_sense) != "":
    syn = best_sense.synset()
    wnet_lem = SV_SENSE_MAP[str(sense)]
    if str(syn.name()) in wnet_lem:
      occ_num=occ_num+1
  total_num=total_num+1
  print('Best sense: ', syn.name(),' Actual sense: ', sense)
  best_sense=""
  max_overlap=0
print('Precision is: ', occ_num/total_num)

