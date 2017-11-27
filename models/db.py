# -*- coding: utf-8 -*-

from apputils import notification, before_trigger_auth, after_trigger_auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# Add extra fields to Auth form (this must be done before auth.define_tables)
auth.settings.extra_fields['auth_user'] = [
    Field('address'),
    Field('city'),
    Field('zip'),
    Field('phone'),
    Field('membership_plan', requires=IS_IN_SET(['Golds', 'Silver', 'Diamond'])),
    Field('agree','boolean',label='I agree to Terms and Conditions',requires=IS_NOT_EMPTY(error_message='You must agree to Terms and Conditions'))
]

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)
db._common_fields.append(auth.signature)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
#mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
#mail.settings.sender = myconf.get('smtp.sender')
#mail.settings.login = myconf.get('smtp.login')
#mail.settings.tls = myconf.get('smtp.tls') or False
#mail.settings.ssl = myconf.get('smtp.ssl') or False

# Send emails with local server for testing PURPOSE
# Command for running local debug server :  python -m smtpd -n -c DebuggingServer localhost:1025

mail.settings.server = 'logging'
mail.settings.sender = 'admin@domain.com'
# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.register_onaccept = lambda form: redirect(URL('welcomeregistered',args=[form.vars.email,]))
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

auth.messages.logged_in = notification('Logged In', 'success')
#print auth.default_messages
auth.messages.registration_pending = notification('Your account registration is pending approval', 'info')
# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

db.auth_user._before_update.append(before_trigger_auth)
db.auth_user._after_update.append(lambda s,f: after_trigger_auth(s,f,mail))


def representfunc(v,r):
    try:
        return XML(v.replace('\n', '<br/>'))
    except Exception as e:
        pass

db.define_table('products',
                Field('pname',notnull=True,label='Product Name'),
                Field('planguage',label='Product Language',requires=IS_IN_SET(['Punjabi','Hindi' ,'English','French','Spanish', 'German'])),
                Field('pcategory',label='Product Category'),
                Field('prating','integer',label='Product Rating'),
                Field('ptype',label='Product Type'),
                Field('pimage','upload',label='Product Image'),
                Field('pdescription','text',label='Product Description'),
                Field('isfeatureproduct','boolean',label='Is this a feature product?',default=False),
                Field('pquantity','integer',label='Product Quantity'),
                Field('pauthor',label='Product Author'),
                Field('ppublisher',label='Product Publisher'),
                auth.signature,
                format='%(pname)s'
               )

db.define_table('borrowedproducts',
                Field('borrower',db.auth_user),
                Field('products',db.products),
                Field('borrowing_date','datetime'),
                Field('return_date','datetime'),
                auth.signature)

db.define_table('wishlist',
                Field('borrower',db.auth_user),
                Field('products',db.products),
                Field('wishlist_date','datetime',label="Date"),
                auth.signature)

db.define_table('updatefeed',
                Field('username'),
                Field('useremail',requires=IS_EMAIL()),
                auth.signature)

db.define_table('productreviews',
                Field('username',db.auth_user),
                Field('products',db.products),
                Field('review_date','datetime'),
                Field('rating','integer'),
                Field('review_text','text'),
                auth.signature)

db.products.pcategory.requires = IS_IN_SET(['Educational & Professional','Fiction & Non Fiction','Philosophy','Religion & Spirituality','Families & Relationship','Reference','Self Help','Hobbies'])
db.products.ptype.requires = IS_IN_SET(['Paperback','Hardcover','Library Binding','Boxed Set','Audiobook','Leather Bound','Board Book'])
db.products.pdescription.represent = representfunc
db.productreviews.review_text.represent = representfunc
