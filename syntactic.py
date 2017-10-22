def parse(nlp, sentence):
    """Parse unicode sentence into a NLTK tree
    using the spacy parser"""
    doc = nlp(sentence)
    trees = [tree(s.root) for s in doc.sents]
    assert len(trees) == 1
    return trees[0]

def tree(node):
    from nltk import Tree
    if node.pos_ in ('VERB', 'NOUN'):
        tag = node.lemma_
    else:
        tag = node.lower_

    if node.n_lefts + node.n_rights > 0:
        return Tree(tag, [tree(child) for child in node.children])
    else:
        return tag



if __name__ == '__main__':
    import spacy
    nlp = spacy.load('en')
    trees = []
    while True:
        new_text = raw_input('> ')
        if not new_text: break
        trees.append(parse(nlp, unicode(new_text)))

    for t in trees:
		from view import *
		createfile(view(t))
		print(t)
		t.pretty_print()
