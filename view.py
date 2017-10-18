def view(tree):
  from nltk import Tree
  start = """digraph G
  {
  node [shape=circle];
  node [style=filled];
  node [fillcolor="#EEEEEE"];
  node [color="#EEEEEE"];
  edge [color="#31CEF0"];"""

  def walk(text, tree):
    #import pdb; pdb.set_trace()
    if type(tree) == unicode:
        return tree
    else:
        for c in tree:
          text += "%s -> %s;\n" % (tree.label(), c if type(c)==unicode else c.label())
          text = walk(text, c)
        return text

  return walk(start, tree) + "\nrankdir=LR;\n}"


if __name__ == '__main__':
    import spacy
    nlp = spacy.load('en')
    from syntactic import parse
    tree = parse(nlp, u'My cat is black')
    print view(tree)
