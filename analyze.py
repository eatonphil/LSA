import sys
import time

import circ
import logisim.core as core

LSA_HEADER = """Logisim Static Analysis - """
LSA_FOOTER = """Generated %s for %s::%s.\n"""
LSA_FORMAT = '.lsa'

TRANSISTORS_HEADER = LSA_HEADER+"""Transistors\n\nCircuit\t\tComponent\tWidth\tNumber of Transistors\n"""
TRANSISTORS_FOOTER = """=============================================================\nTotal\t\t\t\t\t%s\n\n"""+LSA_FOOTER
TRANSISTORS_FILE = 'transistors'+LSA_FORMAT

UNUSED_HEADER = LSA_HEADER+"""Unused Circuits\n\n"""
UNUSED_FOOTER = """\n"""+LSA_FOOTER
UNUSED_FILE = 'unused'+LSA_FORMAT

def total(root):
	a = root['transistors']
	for child in root['children']:
		a += total(child)
	return a

def _dsp(root, file_h, depth=1):
	fname = root['name']
	if len(root['name']) < 8: fname = root['name']+"\t" # for formatting
	if len(root['children']) > 0:
		str_children = sorted([s for s in root['children'] if len(s['children']) == 0])
		dict_children = [s for s in root['children'] if len(s['children']) > 0]
		root['children'] = str_children + dict_children
		file_h.write(fname+'\n')
	else:
		file_h.write('\t\t'+"\t".join([fname, str(root['width']), str(root['transistors'])])+"\n")
	for child in root['children']:
		_dsp(child, file_h)
	if len(root['children']) > 0 and 'root' not in root:
		file_h.write('\t\tSubtotal ('+root['name']+')\t'+str(total(root))+'\n')

def dsp(circuit, circuit_tree):
	with open(TRANSISTORS_FILE, 'w') as f:
		f.write(TRANSISTORS_HEADER)
		circuit_tree['root'] = True
		_dsp(circuit_tree, f)
		f.write(TRANSISTORS_FOOTER % (str(total(circuit_tree)), time.ctime(), sys.argv[1], circuit))

def analyze_transistors(circuit):
	circuit_tree = circ.component(circuit)
	circuit_tree['children'] = circ.count(circ.find(sys.argv[1], circuit), sys.argv[1])
	dsp(circuit, circuit_tree)

def analyze_unused(circuit):
	xmldoc = circ.find(sys.argv[1], circuit)
	unused = circ.unused(xmldoc, sys.argv[1], circuit)
	with open(UNUSED_FILE, 'w') as f:
		f.write(UNUSED_HEADER)
		if len(unused) == 0:
			f.write('No unused circuits.\n')
		else:
			for comp in unused:
				f.write(comp+'\n')
		f.write(UNUSED_FOOTER % (time.ctime(), sys.argv[1], circuit))


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Please provide a file to analyze."
		sys.exit(0)
	try:
		with open(sys.argv[1], 'r') as f:
			f.read()
	except:
		print "Error opening file: %s. File may not exist." % sys.argv[1]
		sys.exit(0)

	circuit = core.MAIN_CIRC
	if len(sys.argv) > 2:
		circuit = sys.argv[2]
	analyze_transistors(circuit)
	analyze_unused(circuit)