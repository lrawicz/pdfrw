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

def girar_core(trailer):
	rotate = 180
	rotate = int(rotate)
	assert rotate % 90 == 0

	pages = trailer.pages
	ranges = []
	for x in range(1, len(pages)):
		if (x%2 == 0):
			ranges.append(x-1)
	for pagenum in ranges:
	    pages[pagenum].Rotate = (int(pages[pagenum].inheritable.Rotate or
	                                     0) + rotate) % 360
	return trailer
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

def girar(path0):
	path1 = '1.%s' % os.path.basename(path0)
	outdata2 = PdfWriter(path1)
	outdata2.trailer = girar_core(PdfReader(path0))
	outdata2.write()
	return path1
def dividir(path_0):
	path2 = '2.' + os.path.basename(path_0)
	writer = PdfWriter(path2)
	for page in PdfReader(path1).pages:
	    writer.addpages(splitpage(page))
	writer.write()
	return path2
def librito(path_0):
	path3 = 'final.' + os.path.basename(path_0)
	ipages = PdfReader(path2).pages


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
# parte 1 - girar
path0 = sys.argv[1]
path1 = girar(path0)
path2 = dividir(path1)
path3 = librito(path2)
os.remove(path1)
os.remove(path2)
# parte 2 - Dividir en dos unspread
# parte 3 - booklet



'''
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input pdf file name")
parser.add_argument("-p", "--padding", action = "store_true",
                    help="Padding the document so that all pages use the same type of sheet")
args = parser.parse_args()
'''
