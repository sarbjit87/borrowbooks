import os
import datetime
import re
import sys
import csv
from PIL import Image, ImageDraw, ImageFont
import random

# Assumption : script is placed inside scripts folder in application
scriptPath = os.path.dirname(os.path.realpath(__file__))
dbPath = os.path.abspath(os.path.join(scriptPath,"../databases"))
libraryPath = os.path.abspath(os.path.join(scriptPath,"../../.."))

sys.path.append(libraryPath)
from gluon import DAL

db = DAL('sqlite://storage.sqlite',folder=dbPath,auto_import=True,debug=True)
#producttable = db['product']

def createImage(imageName,text="Sample Image"):
    fo = open(imageName,'wb')
    size = (400,250)             # size of the image to create
    im = Image.new('RGB', size,(255, 255, 255, 0)) # create the image
    draw = ImageDraw.Draw(im)   # create a drawing object that is
    text_color = (0,0,0)    # color of our text
    text_pos = (150,120) # top-left position of our text
    font = ImageFont.truetype("Arial.ttf", 50)
    # Now, we'll do the drawing:
    draw.text(text_pos, text, fill=text_color)
    del draw # I'm done drawing so I don't need this anymore
    im.save(fo,'JPEG')

for recordno in xrange(1,100):
    record = {}
    record['pname'] = "Book" + str(recordno)
    record['planguage'] = random.choice(['Punjabi','Hindi','English','French','Spanish','German'])
    record['pcategory'] = random.choice(['Educational & Professional','Fiction & Non Fiction','Philosophy','Religion & Spirituality','Families & Relationship','Reference','Self Help','Hobbies'])
    record['ptype'] = random.choice(['Paperback','Hardcover','Library Binding','Boxed Set','Audiobook','Leather Bound','Board Book'])
    record['pdescription'] = "This is sample description for %s. It is published in language %s. It belongs to %s category with type %s." %(record['pname'],record['planguage'],record['pcategory'],record['ptype'])
    record['prating'] = random.randint(1,5)
    record['pquantity'] = random.randint(1,4)
    record['isfeatureproduct'] = random.choice([True,False])
    record['ppublisher'] = "Publisher" + str(random.randint(1,20))
    record['pauthor'] = "Author" + str(random.randint(1,20))
    imgName = "Product" + str(recordno) + ".jpeg"
    imgFullName = os.path.join(os.getcwd(),imgName)
    imgString = "Image for %s" %(record['pname'])
    createImage(imgFullName,imgString)
    stream = open(imgFullName, 'rb')
    record['pimage'] = stream
    #stream.close()
    print "Inserting record : %s " %(str(recordno))
    db.products.insert(**record)
    db.commit()
    #assert False
