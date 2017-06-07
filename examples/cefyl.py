#!/usr/bin/env python

'''
usage:   rotate.py my.pdf rotation [page[range] ...]
         eg. rotate.py 270 1-3 5 7-9

        Rotation must be multiple of 90 degrees, clockwise.

Creates rotate.my.pdf with selected pages rotated.  Rotates all by default.

'''

import sys
import os

from pdfrw import PdfReader, PdfWriter, PageMerge


def splitpage(src):
    ''' Split a page into two (left and right)
    '''
    # Yield a result for each half of the page
    for x_pos in (0, 0.5):
        yield PageMerge().add(src, viewrect=(x_pos, 0, 0.5, 1)).render()


def fixpage(*pages):
    result = PageMerge() + (x for x in pages if x is not None)
    result[-1].x += result[0].w
    return result.render()

def girar(path_0):
	path1 = 'Girar.%s' % os.path.basename(path_0)
	outdata2 = PdfWriter(path1)
	trailer = PdfReader(path_0)
	rotate = 180
	rotate = int(rotate)
	pages = trailer.pages
	ranges = []
	for x in range(0, len(pages)-1):
		if (x%2 != 0):
			ranges.append(x)
	print(ranges)
	for pagenum in ranges:
		pages[pagenum].Rotate = (int(pages[pagenum].inheritable.Rotate or 0) + rotate) % 360

	outdata = PdfWriter(path1)
	outdata.trailer = trailer
	outdata.write()

	return path1
def dividir(path_0):
	path2 =  'Dividir.%s' % os.path.basename(path_0)
	writer = PdfWriter(path2)
	for page in PdfReader(path_0).pages:
	    writer.addpages(splitpage(page))
	writer.write()
	return path2
def subSet(path_0,ranges):
	if not ranges:
	    ranges = [[1, len(pages)]]
	    return path_0
	else:
		ranges = ([int(y) for y in x.split('-')] for x in ranges)
		path2 = 'subset.%s' % os.path.basename(path_0)
		pages = PdfReader(path_0).pages
		outdata = PdfWriter(path2)
		for onerange in ranges:
			onerange = (onerange + onerange[-1:])[:2]
			for pagenum in range(onerange[0], onerange[1]+1):
				outdata.addpage(pages[pagenum-1])
		outdata.write()
		return path2
def librito(path_0):
	path3 = 'final.' + os.path.basename(path_0)
	ipages = PdfReader(path_0).pages


	pad_to = 2

	# Make sure we have a correct number of sides
	ipages += [None]*(-len(ipages)%pad_to)

	opages = []
	while len(ipages) > 2:
	    opages.append(fixpage(ipages.pop(), ipages.pop(0)))
	    opages.append(fixpage(ipages.pop(0), ipages.pop()))
	if (len(ipages)) == 2:
		opages.append(fixpage(None, ipages.pop(0)))
		ipages2 = PdfReader("none.pdf").pages
		opages.append(fixpage(ipages2.pop(0), ipages.pop()))
	opages += ipages

	PdfWriter(path3).addpages(opages).write()
# -----------------------

accion = sys.argv[1];
path0 = sys.argv[2];
ranges = sys.argv[3:];
path1 = path0
#girar
if "C" in accion:  
	path1 = girar(path1)
#subset
if "S" in accion:
	path1 = subSet(path1, ranges)
#dividir
if ("D" in accion) or ("C" in accion):
	path1 = dividir(path1);
#librito
if ("L" in accion) or ("C" in accion):
	path1 = librito(path1);


#C = cefyl
#D = dividir
