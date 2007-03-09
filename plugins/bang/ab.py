#!/usr/bin/env python
"""Addressbook Plugin
!ab [add <name> <address> | remove <name> | list | find <name or address>]"""
import backend

class address(backend.DatabaseObject):
	name = ""
	address = ""
	__namespace__ = ""

def bang(pipein, arguments, event):
	if not arguments:
		return(__doc__, None)

	arguments = arguments.split()

	if arguments[0] == 'add' and len(arguments) == 3:
		addr = address(-1, name = arguments[1], __namespace__ = event.target)

		if len(addr) > 0:
			outstr = "Replacing " + addr.name
		else:
			outstr = "Added"
		addr = address(name = arguments[1], address = arguments[2], __namespace__ = event.target)
		return(outstr, None)

	elif (arguments[0] == 'find' and len(arguments) == 2) or arguments[0] == 'list':
		outstr = []
		
		if arguments[0] == 'find':
			addrs = address(-1, name = arguments[1], __namespace__ = event.target)
			# + address(-1, address = arguments[1])
		else:
			addrs = address(-1, __namespace__ = event.target)

		for each in addrs:
			outstr.append("[" + str(each.id) + "] "+ each.name + " - " + each.address)

		return(outstr, None)

	elif (arguments[0] == 'remove' or arguments[0] == 'delete' or arguments[0] == 'rm'):
		addr = address(-1, name = arguments[1], __namespace__ = event.target)
		if len(addr) > 0:
			addr.drop()
			return ("Removing " + addr.name, None)
		else:
			return ("No records matching " + arguments[1] + " found.", None)

	else:
		return(None, None)
