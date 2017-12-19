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


facts = []
property = []
relations = [
    'european = Relation()','spaniard = Relation() ', 'german = Relation()', 'english = Relation()', 'french = Relation()', 'swede = Relation()',
    'large = Relation()', 'small = Relation()', 'not_large = Relation()', 'not_small = Relation()',
    'animal = Relation()', 'cat = Relation()', 'bird = Relation()', 'dog = Relation()', 'mouse = Relation()',
]
functions = [
    'def european(u): return conde( [spaniard(u)], [german(u)], [english(u)], [french(u)], [swede(u)] )',
    'def not_large(u) : return small(u)', 'def not_small(u): return large(u)', 
    'def animal(u): return conde( [cat(u)], [dog(u)], [bird(u)], [mouse(u)])',
]

ps = []
query = []

ps += resultat[:-1]
query.append(resultat[-1], )

# Iterates the list of rules and facts
# --------------------------------------------------------------------------------------------------------------
for p in ps:
    if p[0] == 'EXISTS':  # Fact
        obj = p[1]
        if p[2][0] == 'AND':
            for q in p[2][1:]:

                prop = q[0]  # Property
                arg = "[" + ', '.join(map(str, q[1:])) + "]"  # Arguments
                #import pdb; pdb.set_trace()

                if not (prop in property):  # If ain't the list, add it
                    relations.append('{} = Relation()'.format(prop))
                    property.append(prop)
                    if prop[:4] == 'not_':  # If it starts with not
                        not_prop = prop[4:]
                        relations.append('{} = Relation()'.format(not_prop))
                        property.append(not_prop)
                    else:
                        relations.append('not_{} = Relation()'.format(prop))
                        property.append('not_{}'.format(prop))

                facts.append("facts({}, {},)".format(prop, arg))
        else:
            print('OR')
    if p[0] == 'FORALL':  # Rule   P(argP) -> Q(argQ)
        obj = p[1]
        if p[2][0] == 'IMPLY':

            P_prop = p[2][1][0]
            Q_prop = p[2][2][0]

            if not (P_prop in property):  # If it's not in the list, add it
                relations.append('{} = Relation()'.format(P_prop))
                property.append(P_prop)
                if P_prop[:4] == 'not_':  # If it starts with not
                    not_P_prop = P_prop[4:]
                    relations.append('{} = Relation()'.format(not_P_prop))
                    property.append(not_P_prop)
                else:
                    relations.append('not_{} = Relation()'.format(P_prop))
                    not_P_prop = "not_{}".format(P_prop)
                    property.append(not_P_prop)

            if not (Q_prop in property):  # If it's not in the list, add it
                relations.append('{} = Relation()'.format(Q_prop))
                property.append(Q_prop)
                if Q_prop[:4] == 'not_':  # If it starts with not
                    not_Q_prop = Q_prop[4:]
                    relations.append('{} = Relation()'.format(not_Q_prop))
                    property.append(not_Q_prop)
                else:
                    relations.append('not_{} = Relation()'.format(Q_prop))
                    not_Q_prop = 'not_{}'.format(Q_prop)
                    property.append(not_Q_prop)

            P_arg = ""
            Q_arg = ""

            for x in p[2][1][1:]:  # Treating functions' arguments
                if obj == x:
                    P_arg += " u{},".format(obj)
                else:
                    P_arg += " '" + x + "'" + ','

            for y in p[2][2][1:]:
                if obj == y:
                    Q_arg += " u{},".format(obj)
                else:
                    Q_arg += " '" + y + "'" + ','

            P_arg = P_arg[:-1]  # Delete the last coma
            P_arg = P_arg[1:]  # and space bar
            Q_arg = Q_arg[:-1]
            Q_arg = Q_arg[1:]

            if P_prop[:4] == 'not_':
                not_P_prop = P_prop[4:]
            else:
                not_P_prop = 'not_{}'.format(P_prop)

            if Q_prop[:4] == 'not_':
                not_Q_prop = Q_prop[4:]
            else:
                not_Q_prop = 'not_{}'.format(Q_prop)

            functions.append("def {}({}): return {}({})".format(Q_prop, Q_arg, P_prop, P_arg))
            functions.append("def {}({}): return {}({})".format(not_P_prop, P_arg, not_Q_prop, Q_arg))

# --------------------------------------------------------------------------------------------------------------
variables = []  # variables = vars(len(variables))
goals = ""

ctd = 0
for q in query:
    if q[0] == 'EXISTS':
        obj = 'u{}'.format(q[1])
        if not (obj in variables):
            variables.append(obj + ', ')
            ctd += 1
        if q[2][0] == 'AND':
            for m in q[2][1:]:
                prop = m[0]
                arg = m[1:]
                str_arg = ""
                for x in range(len(arg)):
                    if arg[x] == q[1]: arg[x] = obj
                    str_arg += arg[x]
                    goals += ' {}({}),'.format(prop, str_arg)
        if q[2][0] == 'OR':
            or_list = []
            for m in q[2][1:]:
                prop = m[0]
                arg = m[1:]
                for x in range(len(arg)):
                    if arg[x] == q[1]: arg[x] = obj
                or_list.append('[{}({})],'.format(prop, arg))
            goals.append("conde({})".format(*or_list))

    if q[0] == 'FORALL':
        obj = 'u{}'.format(q[1])
        if not (obj in variables):
            variables.append(obj + ', ')
            ctd += 1
        if q[2][0] == 'IMPLY':
            P_prop = q[2][1][0]
            P_arg = q[2][1][1]
            Q_prop = q[2][2][0]
            Q_arg = q[2][2][1]

            facts.append("facts({}, ['{}'],)".format(P_prop, P_arg))
            goals += "{}(u{}),".format(Q_prop, q[1])


# --------------------------------------------------------------------------------------------------------------
str_vars = ""
for i in range(len(variables)):  # To string
    str_vars += variables[i]
str1_vars = "[{}] = vars({})".format(str_vars, ctd)
str_goal = "if str(run(0, [{}],{})) == '()': print('False')".format(str_vars, goals)
ss = "else: print('True')"
rs = relations + ["\n"] + facts + ["\n"] + functions + ["\n"] + [str1_vars, str_goal, ss]


def make_file(f_name, *ps):
    with open(f_name, 'w') as f:
        f.write("from kanren import *\n\n")
        for p in ps:
            f.write(p + '\n')


make_file('kk.py', *rs)
#execfile('kk.py')
exec(open("kk.py").read())
