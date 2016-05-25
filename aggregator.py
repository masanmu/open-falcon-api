#!/usr/bin/env python

from core import Open_Falcon_Api
import optparse
import getpass

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
    OptionsParser = optparse.OptionParser
    parser = OptionsParser(usage)

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
            metavar="FILE",help="""Load values from input file.for standard input Each line of file contains whitespace delimited:<numerator>4space<denominator>4space<endpoint>4space<metric>4space<tags>4space<step>
            """)


    options, args = parser.parse_args()
    if not options.server:
        options.server = raw_input("server http:")
    if not options.name:
        options.name = raw_input("username:")
    if not options.password:
        options.password = getpass.getpass()
    if not options.module:
        options.module = raw_input("module:")
    if not options.method:
        options.method = raw_input("method:")

    return options,args

if __name__ == "__main__":

    options,args = get_options()
    name = options.name
    password = options.password
    server = options.server
    module = options.module
    method = options.method

    module_port = port[module]
    openfalconapi = Open_Falcon_Api(server,name,password)

    if options.filename:
        aggregator=dict()
        method=method.replace("/","_")
        with open(options.filename) as f:
            for i in f.xreadlines():
                line = i.split("    ")
                aggregator["numerator"] = line[0]
                aggregator["denominator"] = line[1]
                aggregator["endpoint"] = line[2]
                aggregator["metric"] = line[3]
                aggregator["tags"] = line[4]
                aggregator["step"] = line[5]
                exec "openfalconapi."+method+"(aggregator,module_port)"
