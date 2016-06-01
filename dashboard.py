#!/usr/bin/env python

import getpass
import optparse
import time

from core import Open_Falcon_Api

api_list={
"1":"/api/endpoints?q={endpoint}&tags={tag}&limit={limit}",
"2":"/api/counters",
"3":"/api/tmpgraph",
"4":"/chart",
"5":"/chart/a?id={id}&cf={cf}&start={start}&end={end}&sum={sum}",
"6":"/chart/big",
"7":"/chart/embed",
"8":"/chart/h?id={id}&cf={cf}&start={start}&end={end}&sum={sum}",
"9":"/chart/k?id={id}&cf={cf}&start={start}&end={end}&sum={sum}",
"10":"/charts",
"11":"/graph/<int:gid>/edit",
"12":"/graph/<int:gid>/delete",
"13":"/graph/multi_edit",
"14":"/screen",
"15":"/screen/{sid}",
"16":"/screen/{sid}/clone",
"17":"/screen/{sid}/delete",
"18":"/screen/{sid}/edit",
"19":"/screen/{sid}/graph",
"20":"/screen/add",
"21":"/screen/embed/{sid}" 
}

def get_options():
    usage = "usage: %prog usage"

    OptionParser = optparse.OptionParser
    parser = OptionParser(usage)

    parser.add_option("-u","--user",action="store",type="string",\
            dest="name",help="(REQUIRED)Open-Falcon login user")
    parser.add_option("-p","--password",action="store",type="string",\
            dest="password",help="(REQUIRED)Open-Falcon login user password")
    parser.add_option("-s","--server",action="store",type="string",\
            dest="server",help="(REQUIRED)Open Falcon server")
    parser.add_option("-m","--method",action="store",type="string",\
            dest="method",help="""(REQUIRED)All api listing agent
            "1":"/api/endpoints?q={endpoint}&tags={tag}&limit={limit}"  "2":"/api/counters" "3":"/api/tmpgraph" "4":"/chart"    "5":"/chart/a?id={id}&cf={cf}&start={start}&end={end}&sum={sum}"    "6":"/chart/big"    "7":"/chart/embed"  "8":"/chart/h?id={id}&cf={cf}&start={start}&end={end}&sum={sum}"    "9":"/chart/k?id={id}&cf={cf}&start={start}&end={end}&sum={sum}"    "10":"/charts"  "11":"/graph/<int:gid>/edit"    "12":"/graph/<int:gid>/delete"  "13":"/graph/multi_edit"    "14":"/screen"  "15":"/screen/{sid}"    "16":"/screen/{sid}/clone"  "17":"/screen/{sid}/delete" "18":"/screen/{sid}/edit"   "19":"/screen/{sid}/graph"  "20":"/screen/add"  "21":"/screen/embed/{sid}"
            """)

    options,args = parser.parse_args()

    if not options.server:
        options.server = raw_input("server http:")
    if not options.name:
        options.name = raw_input("username:")
    if not options.password:
        options.password = getpass.getpass()

    return options,args

if __name__ == "__main__":
    options,args = get_options()

    name = options.name
    password = options.password
    server = options.server
   
    openfalconapi = Open_Falcon_Api(server,name,password)

    while 1:
        api_num = raw_input("Choose any one of a list of api:")
        method = api_list[api_num].replace("/","_")
        ts = int(time.time()) 
        data = raw_input("Required to send data:")
        if not data:
            exec "openfalconapi."+method+"(None,8081)"
        else:
            exec "openfalconapi."+method+"(data,8081)"
