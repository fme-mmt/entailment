
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
        

if __name__ == '__main__':
    import spacy
    nlp = spacy.load('en')
    sentences = []
    trees = []
    while True:
        new_text = raw_input('> ')
        if not new_text: break
        sentences.append(parse_sentence(nlp, unicode(new_text)))
        trees.append(parse_tree(nlp, unicode(new_text)))

    for s in sentences:
        print(s.pretty_print())

    for t in trees:
        print(t)
