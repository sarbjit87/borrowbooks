# -*- coding: utf-8 -*-
import paginator as Paginator
import datetime
from apputils import notification

def index():
    query = (db.products.id > 0) & (db.products.isfeatureproduct == True)
    featureproducts = db(query).select(orderby=~db.products.created_on,limitby=(0,4))
    query = (db.products.id > 0)
    recentproducts = db(query).select(orderby=~db.products.created_on,limitby=(0,4))
    categories = ['Educational & Professional','Fiction & Non Fiction','Philosophy','Religion & Spirituality','Families & Relationship','Reference','Self Help','Hobbies']
    return dict(featureproducts=featureproducts,recentproducts=recentproducts,categories=categories)

def membershipplans():
    return dict()

@auth.requires_login()
def myorders():
    query = (db.borrowedproducts.id > 0) & (db.borrowedproducts.borrower == auth.user.id)
    grid = SQLFORM.grid(query=query,details=False,paginate=20,sortable=True,create=False,deletable=False,editable=False,searchable=False,csv=False,
    fields=(db.borrowedproducts.products,db.borrowedproducts.borrowing_date,db.borrowedproducts.return_date),maxtextlengths={'borrowedproducts.products':256})
    return dict(grid=grid)

@auth.requires_login()
def mywishlist():
    query = (db.wishlist.id > 0) & (db.wishlist.borrower == auth.user.id)
    grid = SQLFORM.grid(query=query,details=False,paginate=20,sortable=True,create=False,deletable=True,editable=False,searchable=False,csv=False,
    fields=(db.wishlist.products,db.wishlist.wishlist_date),maxtextlengths={'wishlist.products':256})
    return dict(grid=grid)

def ondelete_test(table_involved,id_of_the_deleted_record):
    query = db[table_involved].id == id_of_the_deleted_record
    queryresult = db(query).select()[0]
    productid = queryresult['products']
    query = db.products.id == productid
    productdetails = db(query).select()[0]
    productquantity = productdetails['pquantity']
    productquantity_up = int(productquantity + 1)
    db(query).update(pquantity=productquantity_up)
    db(db[table_involved].id==id_of_the_deleted_record).delete()

@auth.requires_login()
def addtowishlist():
    pid = request.args[0]
    borrower = auth.user.id
    query = db.wishlist.products == pid
    productcount = len(db(query).select())
    if productcount > 2:
        response.flash = "More than 2 customers has this products in their wishlist"
    row = db.wishlist(borrower=auth.user.id,products=pid)
    print "deubg",row
    if not row:
        db.wishlist.insert(borrower=auth.user.id,
                        products=pid,
                        wishlist_date=datetime.datetime.now())
        session.addtowishlistflash = True
    else:
        session.addtowishlistexistsflash = True
    if request.env.http_referer:
        redirect(request.env.http_referer)
    redirect(URL(request.application,'default','index'))

def __isOrderAuthentic():
    try:
        borrowerplan = auth.user['membership_plan']
        if borrowerplan == "Diamond":
            allowed_products = 20
        elif borrowerplan == "Golds":
            allowed_products = 10
        else:
            allowed_products = 5

        query = (db.borrowedproducts.id > 0) & (db.borrowedproducts.borrower == auth.user.id)
        current_products = db(query).count()
        if current_products < allowed_products:
            return True
        else:
            return False
    except Exception,e:
        print e
        return False

@auth.requires_login()
def conformorder():
    pid = request.args[0]
    query = db.products.id == pid
    productdetails = db(query).select()[0]
    productquantity = productdetails['pquantity']
    session.productid = pid
    form = SQLFORM.factory(
        Field('Name',default=auth.user['first_name']),
        Field('Address',default=auth.user['address']),
        Field('City',default=auth.user['city']),
        Field('Zip',default=auth.user['zip']),
        Field('Email',default=auth.user['email']),
        Field('Product_Name',default=productdetails['pname'],writable=False),
    )
    form.element(_type='submit')['_class']='btn'
    form.element(_type='submit')['_value']='Confirm to Borrow'
    form.add_button(T('Back'),URL(request.application,'default','viewproductdetails',args=[pid]),_class='btn')

    if form.process().accepted:
        if session.productid:
            pid = session.productid
            del session.productid

        query = db.products.id == pid
        productdetails = db(query).select()[0]
        productquantity = productdetails['pquantity']

        if productquantity > 0:
            if __isOrderAuthentic():
                productquantity_up = int(productquantity - 1)
                db(query).update(pquantity=productquantity_up)
                bdate = datetime.datetime.now()
                rdate = bdate + datetime.timedelta(days=15)
                db.borrowedproducts.insert(
                    borrower = auth.user.id,
                    products = pid,
                    borrowing_date = bdate,
                    return_date = rdate
                )
                session.borrowedproductmsg = True
                redirect(URL(request.application,'default','viewproductdetails',args=(pid)))
            else:
                response.flash = notification('Thanks for your interest but your membership plan would not allow you to borrow more products','error')
        else:
            response.flash = notification("Product not available for rent",'error')
    elif form.errors:
        response.flash = notification("Error in form",'error')
    return dict(form=form)

def __compressImage(image):
    try:
        from PIL import Image
        import os
        img_full_path = os.path.join(request.folder,'uploads',image)
        img = Image.open(img_full_path)
        nimg = img.resize((400,250),Image.ANTIALIAS)
        nimg.save(img_full_path,optimize=True,quality=95)
    except Exception,e:
        return

def products():
    recentProductQuery = False
    query = (db.products.id > 0)

    if request.vars.category and request.vars.category != 'None':
        query = query & (db.products.pcategory==request.vars.category)
    elif request.vars.type and request.vars.type != 'None':
        if request.vars.type == "featured":
            query = query & (db.products.isfeatureproduct == True)
        elif request.vars.type == "recent":
            recentProductQuery = True
    elif request.vars.search_param and request.vars.search_text:
        if request.vars.search_param == "name":
            query = query & db.products.pname.like("%%%s%%" %request.vars.search_text)
        elif request.vars.search_param == "category":
            query = query & db.products.pcategory.like("%%%s%%" %request.vars.search_text)
        elif request.vars.search_param == "author":
            query = query & db.products.pauthor.like("%%%s%%" %request.vars.search_text)
        elif request.vars.search_param == "language":
            query = query & db.products.planguage.like("%%%s%%" %request.vars.search_text)
        elif request.vars.search_param == "publisher":
            query = query & db.products.ppublisher.like("%%%s%%" %request.vars.search_text)
        elif request.vars.search_param == "type":
            query = query & db.products.ptype.like("%%%s%%" %request.vars.search_text)
    entriesPerPage = 12
    if not request.vars.page:
        page = 1
    else:
        page = int(request.vars.page)
    start = (page-1) * entriesPerPage
    end = page * entriesPerPage
    totalRecords = db(query).count()
    if recentProductQuery:
        totalRecords = entriesPerPage
        start = 0
        end = entriesPerPage
    products = db(query).select(orderby=~db.products.created_on,limitby=(start,end))
    pagintator = Paginator.pagintation(totalRecords,entriesPerPage,page,request.url,request.vars)
    return dict(products=products,pagintator=pagintator)

@auth.requires_login()
def postreview():
    print request.vars
    review_text = ""
    if request.vars.review_comment:
        review_text = request.vars.review_comment
    if request.vars.review_rating:
        db.productreviews.insert(username = auth.user.id,
                                 review_date=datetime.datetime.now(),
                                 rating=request.vars.review_rating,
                                 products=request.vars.productid,
                                 review_text=review_text
                                 )
    redirect(request.env.http_referer)

def fast_download():
    session.forget(response)
    cache.action(time_expire=604800)(lambda: 0)()
    if request.args(0) != None:
        if not request.args(0).startswith("products.image"):
            return download()
        filename = os.path.join(request.folder,'uploads',request.args(0))
        return response.stream(open(filename,'rb'))

def viewproductdetails():
    if session.addtowishlistflash:
        del session.addtowishlistflash
        response.flash = notification("Product added successfully to your wishlist","success")
    elif session.addtowishlistexistsflash:
        del session.addtowishlistexistsflash
        response.flash = notification("Product already exists in your wishlist","info")
    elif session.borrowedproductmsg:
        del session.borrowedproductmsg
        response.flash = notification("Product borrowed successfully","success")
    pid = request.args[0]
    query = db.products.id == pid
    query1 = db.productreviews.products == pid
    try:
        productdetails = db(query).select()[0]
        reviewdetailsQResults = db(query1).select()
        reviewdetails = []
        for r in reviewdetailsQResults:
            revDetails = {}
            revDetails['review_text'] = r.review_text
            revDetails['username'] = db(db.auth_user.id==int(r.username)).select()[0].first_name
            revDetails['review_rating'] = r.rating
            reviewdetails.append(revDetails)
        return dict(productdetails=productdetails,reviewdetails=reviewdetails)
    except Exception,e:
        return "Invalid Product Selection"

def subscribefeed():
    if request.vars.username and request.vars.useremail:
        db.updatefeed.insert(username=request.vars.username,
                            useremail=request.vars.useremail)
        redirect(URL(request.application,'default','index'))
    else:
        response.flash = notification("Error submitting data","error")

def welcomeregistered():
    user_email = request.args[0]
    greeting_message = "Thanks for registering, your account will be confirmed once payment is recieved"
    mail.send(user_email,"Welcome",greeting_message)
    redirect(URL(request.application,'default','index',vars={'newregistration':'True'}))

# Admin Rules
# ********************************************************************* #

@auth.requires_membership('Admin')
def addproduct():
    form = SQLFORM(db.products)
    form.element(_type='submit')['class']='btn'
    if form.accepts(request.vars,session):
        __compressImage(form.vars.pimage)
        response.flash = notification('Product Database Updated','success')
    elif form.errors:
        response.flash = notification('Please fill in all the required data','error')
    else:
        response.flash = notification('Enter the required details','error')
    return dict(form=form)

@auth.requires_membership('Admin')
def editproduct():
    grid=SQLFORM.grid(db.products)
    return dict(grid=grid)

@auth.requires_membership('Admin')
def productstatus():
    query = db.borrowedproducts.id > 0
    grid=SQLFORM.grid(query=query,paginate=20,sortable=True,create=True,ondelete=ondelete_test,)
    return dict(grid=grid)

@auth.requires_membership('Admin')
def productwishlist():
    query = db.wishlist.id > 0
    grid=SQLFORM.grid(query=query,paginate=20,sortable=True,create=True,ondelete=ondelete_test,)
    return dict(grid=grid)

@auth.requires_membership('Admin')
def managesite():
    return dict()

# ********************************************************************* #


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
