import os
import datetime
import re
import sys
import csv

# Assumption : script is placed inside scripts folder in application
scriptPath = os.path.dirname(os.path.realpath(__file__))
dbPath = os.path.abspath(os.path.join(scriptPath,"../databases"))
libraryPath = os.path.abspath(os.path.join(scriptPath,"../../.."))

sys.path.append(libraryPath)
from gluon import DAL

print dbPath, libraryPath

db = DAL('sqlite://storage.sqlite',folder=dbPath,auto_import=True,debug=True)

def readCsv(csvfile):
    with open(csvfile, 'rb') as f:
        reader = csv.reader(f)
        rownum = 0
        csvRecords = []
        for row in reader:
            csvRecord = {}
            if rownum == 0:
                header = row
            else:
                colnum = 0
                for col in row:
                    #print '%-8s %s' % (header[colnum], col)
                    headcell = header[colnum].split('.')[1]
                    csvRecord[headcell] = col
                    colnum += 1
                csvRecords.append(csvRecord)
            rownum += 1
        return csvRecords

csvrecords = readCsv("db_product.csv")

for csvrecord in csvrecords:
    filename = csvrecord['pimage']
    filename = os.path.join(os.getcwd(),filename)
    stream = open(filename, 'rb')
    csvrecord['pimage'] = stream
    print "Inserting record : %s " %(str(csvrecord['id']))
    db['product'].insert(**csvrecord)
    db.commit()
