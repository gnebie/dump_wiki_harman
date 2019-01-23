import os
import argparse
import re
import xml.etree.ElementTree as etree

def mounthrepl(matchobj):
	if matchobj.group(2) == 'janvier':
		return ("<date>" + matchobj.group(3) + "01" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'février':
		return ("<date>" + matchobj.group(3) + "02" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'mars':
		return ("<date>" + matchobj.group(3) + "03" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'avril':
		return ("<date>" + matchobj.group(3) + "04" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'mai':
		return ("<date>" + matchobj.group(3) + "05" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'juin':
		return ("<date>" + matchobj.group(3) + "06" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'juillet':
		return ("<date>" + matchobj.group(3) + "07" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'août':
		return ("<date>" + matchobj.group(3) + "08" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'septembre':
		return ("<date>" + matchobj.group(3) + "09" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'octobre':
		return ("<date>" + matchobj.group(3) + "10" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'novembre':
		return ("<date>" + matchobj.group(3) + "11" + matchobj.group(1) + "</date>")
	if matchobj.group(2) == 'décembre':
		return ("<date>" + matchobj.group(3) + "12" + matchobj.group(1) + "</date>")
	return ("<date>" + matchobj.group(3) + "0" + matchobj.group(1) + "</date>")

# fonction de l'enfer #perf not found
def replace_line(line):
	# suppression de tout ce qu'il y a apres Notes et références
	cut_index = line.find("== Notes et références ==")
	if (cut_index is not -1):
		line = line[0:cut_index]
	cut_index = line.find("==Notes et références==")
	if (cut_index is not -1):
		line = line[0:cut_index]
	# suppression du complement d'information des blocs [[]]
	while re.search(r'\[\[([^\]]*?)\[\[(.*?)\]\]([^\]]*?)\]\]', line):
		line = re.sub(r'\[\[([^\]]*?)\[\[(.*?)\]\]([^\]]*?)\]\]', r'[[\1\2\3]]', line) # pas opti du tout
	line = re.sub(r'\[\[(Fichier:.*?)\]\]', '', line)
	while re.search(r'\[\[([^\]]*?)\|([^\]]*?)\]\]', line) is not None:
		line = re.sub(r'\[\[([^\]]*?)\|([^\]]*?)\]\]', r'[[\2]]', line) # pas opti du tout
	# Traitement géographique : ils correspondes a des valeurs entre [[]] commenssant par jardin|grottes|parc|chutes ou une majuscule
	# Permet une présélection en enlevant une partie des données n'etant pas géographiques mais
	# Très limité car tous les noms propres sont vu comme des sites géographiques
	line = re.sub(r'\[\[(([A-Z]|jardin|grottes|parc|chutes|col |île).*?)\]\]', r'<geo>\1</geo>', line)
	#Récupération de la date au format {{date|00|mois|0000}}
	#ne prends pas les dates de naissance et de déces
	line = re.sub(r'\{\{date\|([0-9]{1,2})\|(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\|([0-9]{4})\}\}', mounthrepl, line)
	# traitement des éléments de de la page wikipedia pour les transformer en phrases
	line = re.sub(r'\[\[(.*?)\]\]', r'\1', line)
	line = re.sub(r'({{Article détaillé\||{{Ref|{{ref)[^{]*?}}', '', line)
	line = re.sub(r'<ref>.*?</ref>', '', line)
	while re.search(r'{{([^{]*?)(\|)([^{]*?)}}', line):
		line = re.sub(r'{{([^{]*?)(\|)([^{]*?)}}', r'{{\1 \3}}', line)
	line = re.sub(r'{{([^{]*?)}}', r'\1', line)
	line = line.replace('\n\n', '\n')
	return line

def grep_categories(text):
	# recuperation des categories et suppression des valeurs inutiles
	categories = re.findall(r'\[\[Catégorie:.*?\]\]', text)
	cleancategorie = []
	for categorie in categories:
		cleancategorie.append(re.sub(r'\[\[Catégorie:(.*?)(\| |\|\*)?\]\]', r'\1', categorie))
	text = re.sub(r'\[\[Catégorie:.*?\]\]', ' ', text)
	return cleancategorie, text


def strip_tag_name(t):
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

"utf-8"

def write_file(categorie, text, title):
	# codecs.open(pathArticles, "w", ENCODING) as articlesFH
	categorie = etree.Element("categorie")
	article = etree.SubElement(categorie, "article")
	article_title = etree.SubElement(article, "title").text = title
	article_text = etree.SubElement(article, "text").text = text
	tree = etree.ElementTree(categorie)
	etree.dump(tree)
	# print(etree.tostring(tree))
	print("\n\n\n\n")

def parse_file(file_name):
	try:
		title = ''
		text = ''
		print("test")
		i = 0
		for event, elem in etree.iterparse(file_name, events=('start', 'end')):
			tname = strip_tag_name(elem.tag)
			if event == 'start':
				if tname == 'page':
					title = ''
					text = ''
			else:
				a = 0;
				# print(tname)
				if tname == 'title':
					title = elem.text
				elif tname == 'text':
					i += 1
					categorie, text = grep_categories(elem.text)
					# print(categorie)
					text = replace_line(text)
					# print(text)
					write_file(categorie, text, title)
					if i == 2:
						return ;
	except IOError:
		print("Error when file tryed to be open")
		exit(0)

def main():
	try:
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument("file_name", help="File path of the wiki object you find from https://dumps.wikimedia.org/frwiki/latest/")
		args = parser.parse_args()

		parse_file(args.file_name)
		# "/Users/gnebie/goinfre/download/frwiki-latest-pages-articles1.xml-p3p275787"
	# except:
	except IOError:
		print("Unknow Error catch")

if __name__ == '__main__':
	main()
