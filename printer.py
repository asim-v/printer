#!/usr/bin/env python

# import argparse

# # help flag provides flag help
# # store_true actions stores argument as True

# parser = argparse.ArgumentParser()
   
# parser.add_argument('-o', '--output', action='store_true', 
#     help="shows output")

# args = parser.parse_args()

# if args.output:
#     print("This is some output")


 
    

import tempfile
import win32api
import win32print
import os
from PyPDF2 import PdfFileReader,PdfFileWriter
import pathlib 
import tqdm
import time
import sys

a = open('a.txt','w+')
b = open('b.txt','w+')

A = ''
B = ''


def selectFile():
	
	arr = os.listdir('.')
	for i,el in enumerate(arr):
		print('[{}] '.format(i)+el)
	try:
		x = int(input('Select the file to be printed: '))
		return arr[x]
	except:
		print('Entry not valid')



def splitPDF(filename):
	pdf_path = pathlib.Path(filename).absolute()
	pdf = PdfFileReader(str(pdf_path))

	docInfo = pdf.documentInfo #Title creator creationdate producer
	numPages = pdf.getNumPages() #Numero de páginas

	first = []
	second = []

	for i,page in enumerate(pdf.pages):
		if i%2 == 0:			
			first.append(page)
		else:
			second.append(page)

	return (first,second)

def printPage(page):

	try:
		# with Path("first_page.pdf").open(mode="wb") as output_file:
		# 	pdf_writer.write(output_file)
		GHOSTSCRIPT_PATH = "D:\GHOSTSCRIPT\binswin32.exe"
		GSPRINT_PATH = "D:\GSPRINT\gsprint.exe"

		filename = tempfile.mktemp(".pdf")
		pdf_writer = PdfFileWriter()
		pdf_writer.addPage(page)
		with open (filename, "wb") as f:
			pdf_writer.write(f) 
			# os.startfile(filename, "print")
			

			# YOU CAN PUT HERE THE NAME OF YOUR SPECIFIC PRINTER INSTEAD OF DEFAULT
			currentprinter = win32print.GetDefaultPrinter()

			win32api.ShellExecute (0,"printto",filename,'"%s"' % currentprinter,".", 0)
			# win32api.ShellExecute(0, 'open', GSPRINT_PATH, '-ghostscript "'+GHOSTSCRIPT_PATH+'" -printer "'+currentprinter+filename, '.', 0)
	except Exception as e:
		return 1


def menu(first,second,filename):
	print('Imprimir: '+str(filename))
	i = input('Continuar? [y]/[n]: ')
	if i in ['y','Y']:
		for page in tqdm.tqdm(first):
			printPage(page)
			
		print(end='\n')
		i2 = input('Terminado primer lote, imprimir siguiente? [y]/[n]: ')
		if i2 in ['y','Y']:
			print(end='\n')
			for page in tqdm.tqdm(second):

				printPage(page)
				
			print(end='\n')
			print("Terminado exitosamente:)")
		else:
			print("Cancelado")
			return 0

	elif i in ['n','N']:
		return 0


def updateProgress(n):
	for i in range(n):
		j = (i + 1) / n
		sys.stdout.write('\r')
		# the exact output you're looking for:
		sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
		sys.stdout.flush()
		sleep(0.25)





filename = selectFile()
# filename = 'test.pdf' #DEBUG

first,second = splitPDF(filename)
menu(first,second,filename)
# print(first[0]) #DEBUG
# printPage(first[0])



# lenght = 45

# for x in range(lenght):
# 	if x%2 == 0:
# 		A += str(x)+','
# 	else:
# 		B += str(x)+','

# a.write(A[:len(A-1)])
# b.write(B[:len(A-1)])
