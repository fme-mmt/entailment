



import numpy as np

import matplotlib as plt

import pandas as pd

import spacy


from nltk import Tree

nlp = spacy.load('en_core_web_sm')




def to_nltk_tree(node):

    if node.n_lefts + node.n_rights > 0:

        print("%s%s"%(

             node.lemma_, # or "node.orth_," with original form

             ','))

        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])

    else:

        print("%s%s"%(

             node.lemma_, # or "node.orth_," with original form

             ';'))

        return node.orth_




def to_nltk_tree(node):

    if node.n_lefts + node.n_rights > 0:

        print("%s%s"%(

             node.lemma_, # or "node.orth_," with original form

             ','))

        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])

    else:

        print("%s%s"%(

             node.lemma_, # or "node.orth_," with original form

             ';'))

        return node.orth_




def parse_sentence(nlp, sentence):

  """Parse unicode sentence into a NLTK tree

  using the spacy parser"""

  doc = nlp(sentence)

  trees = [tree_sentence(s.root) for s in doc.sents]

  assert len(trees) == 1

  return trees[0]




def tree_sentence(node):

    from nltk import Tree

    if node.pos_ in ('VERB', 'NOUN', 'DET'):

        tag = node.lemma_

    else:

        tag = node.orth_


    if node.n_lefts + node.n_rights > 0:

        return Tree(tag, [tree_sentence(child) for child in node.children])

    else:

        return tag




def parse_tree(nlp, sentence):

    """Parse tag sentence into a NLTK tree

    using the spacy parser"""

    doc = nlp(sentence)

    trees = [tree_tree(s.root) for s in doc.sents]

    assert len(trees) == 1

    return trees[0]




def tree_tree(node):

    from nltk import Tree


    tag = node.tag_


    if node.n_lefts + node.n_rights > 0:

        return Tree(tag, [tree_tree(child) for child in node.children])

    else:

        return tag




def categorical(s):

  if (s == 'every' or s == 'all'):

      return 'FORALL'

  else:

      return 'EXISTS'




def propi(s):

    if (s == 'andreu' or s=='mickey' or s=='jordi' or s=='alejandro'):

        return 'EXISTS'

    else: return 'FORALL'




def conjuncio(s):

    if s == 'FORALL':

        return 'IMPLY'

    else: return 'AND'




def semantic(frase,variable):

  sentences = []

  trees = []

  new_text = frase

  sentences.append(parse_sentence(nlp, (new_text)))

  trees.append(parse_tree(nlp, (new_text)))


  for s in sentences:

      print(s.pretty_print())


  for t in trees:

    print(t)


  for i in range(len(t)-1): 
    if (i>0 and t[i-1]=='DT' and t[i]=='JJ'): t[i]='NN'




  res = []

  count = 0

  count2 = 0

  count4 = 0


  index = 1


  for i in range(len(sentences[0])):

      if (type(sentences[0][0])==str and type(sentences[0][1])==str and count==0):

          res.append(propi(sentences[0][0]))

          res.append(variable)

          index +=1

          res.append([])

          count += 1

          res[index].append(conjuncio(propi(sentences[0][0])))

          res[index].append([sentences[0][0],variable])

      if (type(sentences[0][0])==str and type(sentences[0][1])!=str and count==0):

          res.append(propi(sentences[0][0]))

          res.append(variable)

          index +=1

          res.append([])

          count += 1

          res[index].append(conjuncio(propi(sentences[0][0])))

          res[index].append([sentences[0][0],variable])

      if (type(sentences[0][i])==str and i!=0):
        if (sentences[0][i] == 'not'): 
            
            res[index].append(['not'+'_'+sentences[0][i+1],variable])            
            count4 = 1
        elif count4 != 1: res[index].append([sentences[0][i],variable])

      if (type(sentences[0][i])!=str):

          if(t[i].label()=='NN' or t[i].label()=='NNS'):

              for j in range(len(sentences[0][i])):

                  if(t[i][j]=='DT' and count == 0):

                      res.append(categorical(sentences[0][i][j]))

                      res.append(variable)

                      index +=1

                      res.append([])

                      res[index].append(conjuncio(categorical(sentences[0][0][0])))
                        
                      count += 1

                  else:

                      if (t[i][j]!='DT'):

                          res[index].append([sentences[0][i][j],variable])

              res[index].append([sentences[0][i].label(),variable])

          else:

              for j in range(len(sentences[0][i])):

                  if sentences[0][i][j] == 'not':

                      count2 = 1

                      res[index].append([sentences[0][i][j]+'_'+sentences[0][i].label(),variable])

                  if t[i][j] == 'JJ':

                      res[index].append([sentences[0][i][j],variable])

                      if count2 == 0:

                          res[index].append([sentences[0][i].label(),1])

  return res




premises = []

tesi= ''

resultat = []


while True:

  frase = input('Frase:  ')

  if frase == '': break

  premises.append(frase)


tesi = premises[len(premises)-1]

del premises[len(premises)-1]

variable = 1

for i in range(len(premises)):

  resultat.append(semantic(premises[i],variable))
  variable = variable + 1

resultat.append(semantic(tesi,variable))

print(resultat)

