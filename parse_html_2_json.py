#!/usr/bin/env python3
#coding:utf-8


"""
	@author: Wincel
	@date: May 2016
	@description: Parse html snippets to json
"""


import re
import os
import sys
import bs4
import json
import getopt
from bs4 import BeautifulSoup
from html5lib import HTMLParser


source_file = ""
destination_file = ""


def usage():
	print("parse_html_2_json.py usage :")
	print()
	print("Description: \n\
	read a html file and parse it to json file,also can specify the start point by specify a special feature 'id' in html file byte stream,as same as the end point.")
	print()
	print()
	print("	-h --help 				display  usage")	
	print("	-s source_file 				the source html file to be read and parsed")
	print("	-d destination_file			the destination file to store the result after \n\t\t\t\t\t\tparsing")
	print()
	print("Simple: ")
	print("	parse_html_2_json.py -h")
	print("	parse_html_2_json.py -s test.html -d test.json")
	print("------------------- segmentation line --------------------------")
	print()
	
	
def main():
	global source_file
	global destination_file
	global begin_point
	global end_point
	
	if not len(sys.argv[1:]):
		usage()
		sys.exit(0)
	
	try:
		opts,argv = getopt.getopt(sys.argv[1:],"hs:d:")
	except:
		print()
		print("Uncomplete or incorrect CLI parameters were given!!!")
		print("\n")
		usage()
		sys.exit(0)
		
	for s,c in opts:
		if '-h' in s:
			usage()
			sys.exit(0)
		elif '-s' in s:
			source_file = c
		elif '-d' in s:
			destination_file = c
		else:
			print("Unknown option was given")
			sys.exit(0)

	if len(source_file):
		destination_file = os.path.splitext(destination_file)[0]
		if not os.path.isfile(source_file):
			print("\n[x] Need a file,but just path given or file is not exists")
			sys.exit(0)
		if not len(destination_file):
			print("\n[!] Destination file name is not given,will create the same name of source file")
		ParseJson(source_file,destination_file)
		print()
		print("\n[^_^] Thanks to use!")
		


class ParseJson(object):
	def __init__(self,source,destination=None):
		if len(source):
			self.ppath,file = os.path.split(source)
			self.filename = destination or os.path.splitext(file)[0]
			try:
				buffer = open(source,'r',encoding="utf-8")
				# buffer.encode("utf-8")
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
				rsl = {'tagName':"",'attrs':{},'children':[],"innerHTML":""}
				rsl['tagName'] = stream.name
				for key,val in stream.attrs.items():
					rsl['attrs'][key] = val
				rsl["innerHTML"] = stream.string or ""
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
				print("\n[*] Create jsonify dictionary completely,now parsing to json...")
				self.parseJSON(rsl)
						
	def parseJSON(self,dict):
		if self.ppath:
			file = "{0:}/{1:}.json".format(self.ppath,self.filename)
			buffer = open(file,"w+",encoding="utf-8")
		else:
			file = "{0:}.json".format(self.filename)
			buffer = open(file,"w+",encoding="utf-8")
		json.dump(dict,buffer,ensure_ascii=False)
		print("\n[==>]Parsed completely from %s.html to %s.json" % (self.filename,self.filename))
		print()
		print("[*] Content like :")
		[print("  ",x) for x in dict]
		buffer.close()


if __name__ == "__main__":
	main()
