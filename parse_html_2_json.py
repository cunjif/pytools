#!/usr/bin/env python3
#coding:utf-8


"""
	@author: Wincel
	@date: May 2016
	@description: Parse html snippets to json
"""


import os
import sys
import getopt


source_file = ""
destination_file = ""
begin_point = {}
end_point = {}


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
	print("	-b identitfier 				a special identifier beigin to parse in html file")
	print("	-e endpoint 				an end point to stop parsing in html file ")
	print()
	print("Simple: ")
	print("	parse_html_2_json.py -h")
	print("	parse_html_2_json.py -s test.html -d test")
	print("	parse_html_2_json.py -s test.html -b id='test' -d test")
	print("	parse_html_2_json.py -s test.html -b id='test' -e id='end' -d test")
	print("------------------- segmentation line --------------------------")
	print()
	print("\t\t\tThanks to use!")
	
	
def main():
	global source_file
	global destination_file
	global begin_point
	global end_point
	
	if not len(sys.argv[1:]):
		usage()
		sys.exit(0)
	
	try:
		opts,argv = getopt.getopt(sys.argv[1:],"hs:b:e:d:")
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
		elif '-b' in s:
			begin_point = c
		elif '-e' in s:
			end_point = c
		else:
			print("Unknown option was given")
			sys.exit(0)

	if len(source_file) and len(destination_file):
		with open(source_file) as f:
			page = f.read()
			
		
	
	
	

if __name__ == "__main__":
	main()
