import sys

import xml.etree.cElementTree as ET

from logisim import core
import stdl

def get(xmldoc):
	return ET.ElementTree(file=xmldoc).getroot()

def iterate(xmlroot, next_sibling, condition, function):
	_break = False
	if condition(xmlroot):
		_break = function(xmlroot, next_sibling)
	if not _break:
		for index, child in enumerate(xmlroot.getchildren()):
			next_sibling = xmlroot.getchildren()[index+1] if index+1 != len(xmlroot.getchildren()) else None
			iterate(child, next_sibling, condition, function)

def find(xmldoc, component=core.MAIN_CIRC):
	_component = [None]

	def condition(xmlroot):
		return (xmlroot is not None) and \
			   (xmlroot.tag == core.CIRCUIT_TAG) and \
			   (xmlroot.attrib[core.NAME_ATTR] == component)

	def function(xmlroot, next_sibling):
		_component[0] = xmlroot
		return True

	_xmldoc = xmldoc
	if type(xmldoc) == type(''):
		_xmldoc = get(xmldoc)
	iterate(_xmldoc, None, condition, function)
	return _component[0]


def get_width(xmlroot):
	for child in xmlroot.getchildren():
		if core.NAME_ATTR in child.attrib and child.attrib[core.NAME_ATTR] == core.WIDTH_ATTR_VAL:
			return int(child.attrib[core.VAL_ATTR])
	return 1

def write(file_h, string):
	if file_h is not None:
		file_h.write(string)

def circuits(_component):
	if type(_component) == type([]):
		names = []
		for child in _component:
			names += circuits(child)
	else:
		names = [_component['name']]
		for child in _component['children']:
			names += circuits(child)
	return names

def increase(_component):
	return component(
		_component['name'],
		_component['width'],
		_component['inputs'],
		_component['transistors'],
		_component['count'] + 1,
		_component['children']
	)

def component(name, width=1, inputs=2, transistors=0, count=1, children=[]):
	return {'name': name, 'width': width, 'inputs': inputs, 'transistors': transistors, 'count': count, 'children': children}

def count_fun(xmldoc):
	_count = [0]

	def condition(xmlroot):
		return (xmlroot is not None) and (xmlroot.tag == core.COMP_TAG)

	def function(xmlroot, next_sibling):
		if xmlroot.attrib[core.NAME_ATTR] == core.TRANSISTOR_ATTR_VAL:
			_count[0] += 1
		elif core.LIB_ATTR not in xmlroot.attrib:
			_count[0] += count_fun(find(stdl.GATE_CIRCS, xmlroot.attrib[core.NAME_ATTR]))

	iterate(xmldoc, None, condition, function)
	return _count[0]

def count(xmldoc, filename):
	children = {}

	def condition(xmlroot):
		return (xmlroot is not None) and \
			   (xmlroot.tag == core.COMP_TAG) and \
			   (((core.LIB_ATTR in xmlroot.attrib) and \
			    (int(xmlroot.attrib[core.LIB_ATTR]) > core.WIRING_ATTR_VAL)) or \
			   (core.LIB_ATTR not in xmlroot.attrib)) and \
			   xmlroot.attrib[core.NAME_ATTR] not in core.NAME_BLACKLIST

	def function(xmlroot, next_sibling):
		name = xmlroot.attrib[core.NAME_ATTR]
		width = get_width(xmlroot)
		inputs = 1
		_component = component(name, width)
		lookup, error = stdl.component(name, width, inputs, False)
		if lookup is not False:
			name, location = stdl.component(name, width, inputs)
			if location == stdl.GATE_CIRCS:
				gate_c = count_fun(find(location, name))
				_component['transistors'] = gate_c
		else:
			location = filename
		if location != stdl.GATE_CIRCS:
			comp = find(location, name)
			if not comp:
				print stdl.COMP_NOT_FOUND_ERROR % (name, width, inputs, filename)
				return False
			gate_c = count(comp, location)
			_component['children'] = gate_c
		if name in children:
			children[name] = increase(children[name])
		else:
			children[name] = _component

	iterate(xmldoc, None, condition, function)
	return children.values()

def unused(xmldoc, filename, circuit):
	_circuits = []
	used = count(xmldoc, filename)

	def condition(xmlroot):
		return (xmlroot is not None) and \
			   (xmlroot.tag == core.CIRCUIT_TAG) and \
			   (xmlroot.attrib[core.NAME_ATTR] not in circuits(used)) and \
			   (xmlroot.attrib[core.NAME_ATTR] != circuit)

	def function(xmlroot, next_sibling):
		_circuits.append(xmlroot.attrib[core.NAME_ATTR])

	iterate(get(filename), None, condition, function)
	return _circuits