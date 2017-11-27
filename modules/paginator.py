# MIT License
#
# Copyright (c) 2017, Sarbjit Singh, www.singhsarbjit.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math
from gluon import *

def _getACFfromURL(url):
    "Returns Application, Controller & Function for a URL"
    a,b,c,d = url.split('/')
    return b,c,d

def pagintation(total,entriesPerPage,currentPage,requestURL,params):
    numberPages = int(math.ceil(total/float(entriesPerPage)))
    a,c,f = _getACFfromURL(requestURL)
    argDict = dict(params)
    htmlResult = '<ul class="pagination">'
    if numberPages <= 10:
        startIndex = 1
        endIndex =  numberPages+1
    else:
        if currentPage <= 6:
            startIndex = 1
            endIndex = 11
        elif (currentPage + 4 >= numberPages):
            startIndex = numberPages - 9
            endIndex = numberPages + 1
        else:
            startIndex = currentPage - 5
            endIndex = currentPage + 5
    if currentPage != 1:
        argDict['page']=currentPage-1
        htmlResult = htmlResult + '<li><a href="' + URL(a=a,c=c,f=f,vars=argDict) + '">Prev</a></li>'
    for p in range(startIndex,endIndex):
        argDict['page']=p
        if currentPage == p:
            htmlResult = htmlResult + '<li class="active"><a href="' + URL(a=a,c=c,f=f,vars=argDict) + '">{0}</a></li>'.format(p)
        else:
            htmlResult = htmlResult + '<li><a href="' + URL(a=a,c=c,f=f,vars=argDict) + '">{0}</a></li>'.format(p)
    if currentPage != numberPages:
        argDict['page']=currentPage+1
        htmlResult = htmlResult + '<li><a href="' + URL(a=a,c=c,f=f,vars=argDict) + '">Next</a></li>'
    htmlResult += '</ul>'
    return htmlResult

# Example Usage
########## Controller ##########
# def products():
#     entriesPerPage=12
#     if not request.vars.page:
#         page = 1
#     else:
#         page = int(request.vars.page)
#     start = (page-1) * entriesPerPage
#     end = page * entriesPerPage
#     totalRecords = db(db.products.id > 0).count()
#     query = (db.products.id > 0)
#     products = db(query).select(orderby=~db.products.id,limitby=(start,end))
#     pagintator = Paginator.pagintation(totalRecords,entriesPerPage,page,request.url)
#     return dict(products=products,pagintator=pagintator)

########## Views ##########
# <div class="text-center">
#    {{=XML(pagintator)}}
# </div>
