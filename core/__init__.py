#!/usr/bin/env python

import urllib2
import urllib
import cookielib
import optparse

class Open_Falcon_Api(object):
    def __init__(self,url,user,password):
        self.url= url
        loginurl = self.url+":1234/auth/login"
        self.user = user
        self.password = password

        self.login(loginurl)

    def login(self,loginurl):
        self.request_data={
                "name":self.user,
                "password":self.password,
                }
        try:
            cookie = cookielib.CookieJar()
            handler = urllib2.HTTPCookieProcessor(cookie)
            self.opener = urllib2.build_opener(handler)
            self.auth = self.opener.open(loginurl,urllib.urlencode(self.request_data))
        except Exception as e:
            print "Error:",e

    def deal_request(self,method,params,port):
        self.request_data = params
        method_url = self.url+":"+str(port)+"/"+method.replace("_","/")
        try:
            if self.request_data:
                response = self.opener.open(method_url,urllib.urlencode(self.request_data))
            else:
                response = self.opener.open(method_url)
            return response.read() 
        except Exception as e:
            print "Error:",e
    def __getattr__(self,method):
	def func(params,port):
		params = params
                port = port
		return self.deal_request(method,params,port)
	return func
