import spacy
from nltk import Tree
nlp = spacy.load('en')

introd = "Analysis syntactic"
l = []
while introd != "":
    introd = raw_input()
    doc = nlp(u""+introd)
    def tree(node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(node.orth_, [tree(child) for child in node.children])
        else:
            return node.orth_
    [l.append(tree(sent.root)) for sent in doc.sents]
