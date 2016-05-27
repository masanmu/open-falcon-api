#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from core import Open_Falcon_Api

import optparse
import getpass
import os

port = {
        "agent":1988,
        "alarm":9912,
        "dashboard":8081,
        "fe":1234,
        "graph":6071,
        "hbs":6031,
        "judge":6081,
        "links":5090,
        "portal":5050,
        "task":8002,
        "transfer":6060,
        "query":9966
        }

def get_options():
	usage = "usage: %prog [options]"
	OptionParser = optparse.OptionParser
	parser = OptionParser(usage)

	parser.add_option("-m","--module",action="store",type="string",\
        	dest="module",help="""(REQUIRED)Open Falcon module.
Posible values:
agent - 1988:
alarm - 9912:
dashboard - 8081:
fe - 1234:
graph - 6071:
hbs - 6031:
judge - 6081:
links - 5090:
portal - 5050:
task - 8002:
transfer - 6060:
query - 9966:
""")
    	parser.add_option("-M","--method",action="store",type="string",\
                dest="method",help="(REQUIRED)Open Falcon Api method.")
    	parser.add_option("-u","--user",action="store",type="string",\
            dest="name",help="(REQUIRED)Open-Falcon login user")
    	parser.add_option("-p","--password",action="store",type="string",\
            dest="password",help="(REQUIRED)Open-Falcon login user password")
    	parser.add_option("-s","--server",action="store",type="string",\
            dest="server",help="(REQUIRED)Open Falcon server")
    	parser.add_option("-f","--file",dest="filename",\
            metavar="FILE",help="""Load values from input file.
            for standard input Each line of file contains whitespace delimited:
            <title>4space<hosts>4space<counters>4space<timespan>4space<graph_type>4space<method>
            (graph_type:
                h->endpoint view,k->counter view,a->Combined view 
            method:
                SUM or " ")""")
        
        options,args = parser.parse_args()
        if not options.name:
            options.name = raw_input("Name:")
        if not options.password:
            options.password = getpass.getpass("Password:")
        if not options.server:
            options.server = raw_input("Server HTTP:")
        if not options.method:
            options.method = raw_input("method:")
        if not options.module:
            options.module = raw_input("module:")

        return options,args
if __name__=="__main__":
        options,arsg = get_options()
        name = options.name
        password = options.password
        server = options.server
        method = options.method
        module = options.module

        of = Open_Falcon_Api(server,name,password)
        module_port = port[module]
        
        if options.filename:
            data = dict()
            method = method.replace("/","_")
            with open(options.filename) as f:
                for line in f.xreadlines():
                    try:
                        content = line.rstrip("\n").split("    ")
                        data["title"] = content[0]
                        data["hosts"] = content[1].replace(",","\n")
                        data["counters"] = content[2].replace(",","\n")
                        data["timespan"] = content[3]
                        data["graph_type"] = content[4]
                        data["method"] = content[5]
                    except Exception as e:
                        pass
            print data
            exec "of."+method+"(data,module_port)"
        else:
            data = dict()
            data["title"] = raw_input("title:")
            data["hosts"] = raw_input("hosts:")
            data["counters"] = raw_input("counters:")
            data["timespan"] = raw_input("timespan:")
            data["graph_type"] = raw_input("graph_type:")
            data["method"] = raw_input("method:")
            exec "of."+method+"(data,module_port)"
