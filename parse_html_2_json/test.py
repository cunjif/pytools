#!/usr/bin/env python3
#coding:utf-8


"""
	@author: Wincel
	@date: 
	@description: 
"""

import re
import os
import sys
import bs4
import json
from bs4 import BeautifulSoup
from html5lib import HTMLParser


class ParseJson(object):
	def __init__(self,buffer):
		if len(buffer):
			if not os.path.isfile(buffer):
				print("[*]Please enter a real physical file")
				sys.exit(0)
			self.ppath,file = os.path.split(buffer)
			self.filename = os.path.splitext(file)[0]
			try:
				buffer = open(buffer,'r')
				new_buffer = buffer.read()
				buffer.close()
			except FileNotFoundError as e:
				print(e)
				sys.exit(0)
			self.parseDict(new_buffer)
	
	def parseDict(self,stream):
		def walk(stream):
			rtag = re.compile(r'(script)|(link)')
			if stream.name == '[document]':
				for child in stream.children:
					if child.name:
						tmp = walk(child)
						if tmp:
							return tmp
				return {}
			elif stream.name == 'html':
				rsl = []
				for child in stream.children:
					if child.name:
						tmp = walk(child)
						if tmp:
							rsl.extend(tmp)
				return rsl
			elif stream.name == 'head':
				return
			elif stream.name == 'body':
				rsl = []
				for child in stream.children:
					if child.name:
						tmp = walk(child)
						if tmp:
							rsl.append(tmp)
				return rsl							
			elif isinstance(stream,bs4.element.Tag) \
			and rtag.match(stream.name):
				return
			elif isinstance(stream,bs4.element.NavigableString):
				return
			else:
				rsl = {'tagName':"",'attrs':{},'children':[]}
				rsl['tagName'] = stream.name
				for key,val in stream.attrs.items():
					rsl['attrs'][key] = val
				if stream.children:
					for child in stream.children:
						tmp = walk(child)
						if len(rsl['tagName']) and tmp:
							rsl['children'].append(tmp)
				return rsl	
							
		b = BeautifulSoup(stream,'html5lib')		
		if(b):
			rsl = walk(b)
			if(rsl):
				self.parseJSON(rsl)
						
	def parseJSON(self,dict):
		if self.ppath:
			file = "{0:}/{1:}.json".format(self.ppath,self.filename)
			buffer = open(file,"w+")
		else:
			file = "{0:}.json".format(self.filename)
			buffer = open(file,"w+")
		
		json.dump(dict,buffer)
		buffer.close()
		
		print("[==>]Parsed completely from %s.html to %s.json" % (self.filename,self.filename))
		print()
		print("[*] Content like :")
		[print("  ",x) for x in dict]
		

if __name__ == "__main__":
	ParseJson('index.html')
		# print(dir(b))
		# nodes = b.body.contents		
		# for child in nodes:
			# print(len(child))
		