import os
import argparse
import re

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
	newline = re.sub(r'\[\[(.*?)\]\]', r'<geo>\1</geo>', line)
	newline2 = re.sub(r'\{\{date\|([0-9]{1,2})\|(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\|([0-9]{4})\}\}', mounthrepl, newline)
	return newline2


def parse_file(file_name):
	try:
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
	except:
		print("Error when file tryed to be open")
		exit(0)

def main():
	try:
		parse_file("/Users/gnebie/goinfre/download/frwiki-latest-pages-articles1.xml-p3p275787")
	except:
		print("Unknow Error catch")

if __name__ == '__main__':
	main()
