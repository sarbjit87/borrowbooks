from gluon import *

def notification(message, mtype):
    a = "<script>\n"
    a += "$(\"notify\").ready(function() {\n"
    a += "toastr.options.timeOut = 3000; // 1.5s\n"
    a += "toastr.{mtype}('{message}');\n".format(mtype=mtype, message=message)
    a += "$('#linkButton').click(function() {\n"
    a += "toastr.success('Click Button');\n"
    a += "});\n"
    a += "});\n"
    a += "</script>"
    a = XML(a)
    return a

def before_trigger_auth(s,f):
    try:
        current.session.before_rkey = s.select().first().registration_key
    except Exception,e:
        print e
        pass

def after_trigger_auth(s,f,mail):
    try:
        rkey = f['registration_key']
        if current.session.before_rkey == "pending" and rkey == "":
            mailsender = mail
            del current.session.before_rkey
            ruseremail = s.select().first().email
            greeting_message = "We have confirmed your payment, yout account is now active."
            mail.send(ruseremail,'Welcome',greeting_message)
    except Exception as e:
        print e
        pass
