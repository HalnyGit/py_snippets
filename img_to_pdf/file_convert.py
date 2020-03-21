# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 20:11:19 2020

@author: Komp
"""

from PIL import Image
import glob
import os
from PyPDF4 import PdfFileReader, PdfFileMerger


#Code for converting and merging from jpg files to pdf.
#Assume file names are integers

path = 'C:\\Users\\Komp\\Documents\\wsip\\'
ext = '*.jpg'
new_ext = '.pdf'
pathfiles = path + ext

print('Converting files from {0} to {1}...'.format(ext, new_ext))

for infile in glob.glob(pathfiles):
    f_path, f_name = os.path.split(infile)
    new_name = f_name[:-4]
    new_file_path = f_path + '\\' + new_name + new_ext
    im = Image.open(infile)
    im.save(new_file_path, 'pdf')
    im.close()

print('Done')

print('Grouping and saving pdf files...')

new_pathfiles = path + '*' + new_ext
file_groups = [1, 17, 34, 51, 64, 81]
pdfs = {}

for pdf_file in glob.glob(new_pathfiles):
    f_path, f_name = os.path.split(pdf_file)
    name, *res = os.path.splitext(f_name)
    pdfs[int(name)] = pdf_file

ranges = []
for i in range(len(file_groups)-1):
    r = file_groups[i], file_groups[i+1]
    ranges.append(r)
    

groups = {}

n = 1
for r in ranges:
    for i in range(*r):
        file = pdfs.get(i, 'None')
        if file != 'None':
            groups.setdefault(n, []).append(file)
    n+=1
        
for group, files in groups.items():
    merger = PdfFileMerger()
    for file in files:
        merger.append(file)
    output_path = path + 'merged\\' + str(group) + new_ext
    merger.write(output_path)
    merger.close()
    
print('Completed')

            
    
    


    

    
    


