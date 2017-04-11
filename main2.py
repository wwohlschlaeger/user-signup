#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
USER_PW = re.compile(r"^.{3,20}$")
USER_EM = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

errorsDict={"err_mass1":"","err_mass2":"","err_mass3":"","err_mass4":""}

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">User-Signup</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        name_form = """
            <form action="/ver" method="post">
            <label>
                Enter your name:
                <input type="text" name="user_name"/>
            </label>
            </form>
            """+errorsDict["err_mass1"]
        password_form="""
            <form action="/ver" method="post">
            <label>
                Enter your password:
                <input type="text" name="user_password"/>
            </label>
            </form>
            """+errorsDict["err_mass2"]
        passver_form="""
            <form action="/ver" method="post">
            <label>
                Re-enter your password:
                <input type="text" name="passver"/>
            </label>
            </form>
            """ #+errorsDict["err_mass4"]
        email_form="""
            <form action="/ver" method="post">
            <label>
                Enter your email:
                <input type="text" name="user_email"/>
            </label>
            <input type="submit" value="Submit"/>
        </form>
        """+errorsDict["err_mass3"]
        error1=errorsDict["err_mass1"]
        error2=errorsDict["err_mass2"]
        error3=errorsDict["err_mass3"]
        error4=errorsDict["err_mass4"]

        if error1 != "":
            err_mass1= '<p class="error">'+error1+'</p>'
        else:
            err_mass1=''
        if error2 != "":
            err_mass2='<P class="error">'+error2+'</p>'
        else:
            err_mass2=''
        if error3 != "":
            err_mass3='<p class="error">'+error3+'</p>'
        else:
            err_mass3= ''
        if error4 != "":
            err_mass4='<p class="error">'+error4+'</p>'
        else:
            err_mass4= ''

        page_content= page_header+name_form+err_mass1+password_form+err_mass2+passver_form+err_mass4+email_form+err_mass3+page_footer
        self.response.write(page_content)

class verification(MainHandler):
    def post(self): #took errorsDict out of the passed params
        username= self.request.get("user_name")
        username= cgi.escape(username)
        userpassword= self.request.get("user_password")
        userpassword= cgi.escape(userpassword)
        verpass= self.request.get("passver")
        verpass= cgi.escape(verpass)
        email= self.request.get("user_email")
        email= cgi.escape(email)

        self.response.write(errorsDict)
        error_element1= USER_RE.match(username)

        if not error_element1:
            errorsDict["err_mass1"]="This is not a valid user name."
        #else:
            #errorsDict["err_mass1"]=""
        error_element2= USER_PW.match(userpassword)
        if not error_element2:
            errorsDict["err_mass2"]="This is not a valid password."
        #else:
            #errorsDict["err_mass2"]=""
        error_element3= USER_EM.match(email)
        if not error_element3:
            errorsDict["err_mass3"]="This is not a valid email."
        #else:
            #errorsDict["err_mass3"]=""
        if userpassword != verpass:
            errorsDict["err_mass4"]="The passwords do not match."
        #else:
            #errorsDict["err_mass4"]= ''
        self.redirect('/?errorsDict')

#    def valid_username(username):
        #uname= USER_RE.match(username)
        #error1 = self.request.get("error")
        #if error1:
            #error_esc1 = cgi.escape(error1, quote=True)
            #error_element1 = '<p class="error">' + error_esc1 + '</p>'
        #else:
            #error_element1 = ''
#      return USER_RE.match(username)


#    def valid_password(userpassword):
#      return USER_PW.match(userpassword)

#    def valid_email(email):
#      return USER_EM.match(email)


#class ErrorPage(webapp2.RequestHandler):
#    def get(self):
#        if error:
#            error_esc=cgi.secape(error, quote=True)
#            error_element="<p class=error>" + error_esc + "</p>"
#        elif terriblemovie:
#            error_esc=cgi.secape(error, quote=True)
#            error_element='<p class="error">Trust me you do not want to add that movie</p>'
#        else:
#            error_element= ""

#        errorResponseMsg = "<div style='color:red; font-size:60px'>" + "You Suck!" + "</div>"
#        ERM = errorResponseMsg + "<form action = '/'><input type='submit'/></form>"
#        self.response.write(errorResponseMsg)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/ver', verification)
], debug=True)
