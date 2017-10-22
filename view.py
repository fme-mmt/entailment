def view(tree):
	from nltk import Tree
	start = """digraph G\n{\n node [shape=circle];\n node [style=filled];\n node [fillcolor="#EEEEEE"];\n node [color="#EEEEEE"];\n edge [color="#31CEF0"];\n"""
	return createfile(start + walk("", tree) + " rankdir=LR;\n}")

def walk(text, tree):
    #import pdb; pdb.set_trace() for run pass by pass
    #falta arreglar recurrencia
    for c in tree:
		text += " %s -> %s;\n" % (tree.label(), c if type(c)==unicode else c.label())
		if type(c) != unicode:
			text += walk(text, c)
    return text
    
def createfile(text):
	file = open("viewgraph2.dot","w")
	file.write(str(text))
	file.close()
	lines_seen = set() # holds lines already seen
	outfile = open("viewgraph.dot", "w")
	for line in open("viewgraph2.dot", "r"):
		if line not in lines_seen: # not a duplicate
			outfile.write(line)
			lines_seen.add(line)
	outfile.close()
	from subprocess import check_call
	check_call(['dot','-Tpng','viewgraph.dot','-o','viewgraph.png'])
	from PIL import Image
	img = Image.open('viewgraph.png')
	img.show()
	return;

if __name__ == '__main__':
    import spacy
    nlp = spacy.load('en')
    from syntactic import parse
    #falta enllasssar amb programa syntactic.py
    tree = parse(nlp, u'My black cat has some pizza')
    view(tree)
        
#Millores a fer: no haver de crear dos documents per borrar linies
#repetides, 
