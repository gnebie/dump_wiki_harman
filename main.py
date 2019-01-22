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

def replace_line(line):
	newline = re.sub(r'\[\[(([A-Z]|jardin|grottes|parc|chutes).*?)\]\]', r'<geo>\1</geo>', line)
	newline2 = re.sub(r'\{\{date\|([0-9]{1,2})\|(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\|([0-9]{4})\}\}', mounthrepl, newline)
	return newline2

def grep_categories(text):
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

def parse_file(file_name):
	try:
		print("test")
		i = 0
		for event, elem in etree.iterparse(file_name, events=('start', 'end')):
			i += 1
			tname = strip_tag_name(elem.tag)

			if event == 'start':
				if tname == 'page':
					title = ''
					# id = -1
					# redirect = ''
					# inrevision = False
					# ns = 0
				elif tname == 'revision':
					# Do not pick up on revision id's
					inrevision = True
			else:
				a = 0;
				# print(tname)
				if tname == 'title':
					# print("title " + elem.text)
					title = elem.text
				elif tname == 'text':
					categorie, text = grep_categories(elem.text)
					print(categorie)
					text = replace_line(text)
					# print(text)
			if (i == 1000):
				return
				# elif tname == 'id' and not inrevision:
				# 	id = int(elem.text)
				# elif tname == 'redirect':
				# 	redirect = elem.attrib['title']
				# elif tname == 'ns':
				# 	ns = int(elem.text)
				# elif tname == 'page':
				# 	print("page " + elem.text)
				# 	totalCount += 1
				# 	if ns == 10:
				# 		templateCount += 1
				# 		templateWriter.writerow([id, title])
				# 	elif len(redirect) > 0:
				# 		articleCount += 1
				# 		articlesWriter.writerow([id, title, redirect])
				# 	else:
				# 		redirectCount += 1
				# 		redirectWriter.writerow([id, title, redirect])


		i = 0
		with open(file_name, 'r') as f:
			for line in f:
				print (i)
				newline = replace_line(line)
				print(newline)
				i += 1
				if (i == 5890):
					break ;
		f.close();
	except IOError:
		print("Error when file tryed to be open")
		exit(0)
	# except:
	# 	print("Error when file tryed to be open")
	# 	exit(0)

def main():
	try:
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument("file_name", help="File path")
		args = parser.parse_args()

		parse_file(args.file_name)
		# "/Users/gnebie/goinfre/download/frwiki-latest-pages-articles1.xml-p3p275787"
	# except:
	except IOError:
		print("Unknow Error catch")

if __name__ == '__main__':
	main()
