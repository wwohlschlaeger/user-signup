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

        #if errorsDict['err_mass1'] != "":
        #    errorsDict['err_mass1']= '<p class="error">'+errorsDict['err_mass1']+'</p>'
        #if errorsDict['err_mass2'] != "":
        #    errorsDict['err_mass2']='<p class="error">'+errorsDict['err_mass2']+'</p>'
        #if errorsDict['err_mass3'] != "":
        #    errorsDict['err_mass3']='<p class="error">'+errorsDict['err_mass3']+'</p>'
        #if errorsDict['err_mass4'] != "":
        #    errorsDict['err_mass4']='<p class="error">'+errorsDict['err_mass4']+'</p>'

        user_form = """
            <form action="/verified" method="post">
            <label>
                Enter your name:
                <input type="text" name="user_name" />"""+errorsDict["err_mass1"]+"""
            </label><br>
            <label>
                Enter your password:
                <input type="password" name="user_password" value = ""/>"""+errorsDict["err_mass2"]+"""
            </label><br>
            <label>
                Re-enter your password:
                <input type="password" name="passver" value=""/>"""+errorsDict["err_mass4"]+"""
            </label><br>
            <label>
                Enter your email:
                <input type="text" name="user_email"/>"""+errorsDict["err_mass3"]+"""
            </label><br>
            <br><input type="submit" value="Submit"/>
        </form>
        """

        page_content= page_header+user_form+page_footer
        self.response.write(page_content)

class verification(MainHandler):
    def post(self):
        username= self.request.get("user_name")
        username= cgi.escape(username)
        userpassword= self.request.get("user_password")
        userpassword= cgi.escape(userpassword)
        verpass= self.request.get("passver")
        verpass= cgi.escape(verpass)
        email= self.request.get("user_email")
        email= cgi.escape(email)
        passfail=False

        if not USER_RE.match(username):
            errorsDict["err_mass1"]="This is not a valid user name."
            passfail=True
        else:
            errorsDict["err_mass1"]=""

        if not USER_PW.match(userpassword):
            errorsDict["err_mass2"]="This is not a valid password."
            passfail=True
        else:
            errorsDict["err_mass2"]=""

        if not USER_EM.match(email):
            errorsDict["err_mass3"]="This is not a valid email."
            passfail=True
        else:
            errorsDict["err_mass3"]=""

        if userpassword != verpass:
            errorsDict["err_mass4"]="The passwords do not match."
            passfail=True
        else:
            errorsDict["err_mass4"]=""


        if passfail == True:
            self.redirect('/?errorsDict')
        else:
            #username=self.request.get('user_name')
            self.response.write('Welcome '+username+'!')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/verified', verification)
], debug=True)
