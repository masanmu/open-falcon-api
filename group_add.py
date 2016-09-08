#!/usr/bin/env python

from core import Open_Falcon_Api
import optparse
import getpass
import os
import json
import urllib2

def get_options():
    usage = "usage: %prog [options]"
    OptionsParser = optparse.OptionParser
    parser = OptionsParser(usage)

    parser.add_option("-a","--api",action="store",type="string",\
                dest="api",help="(REQUIRED)Open Falcon Api method.")
    parser.add_option("-u","--user",action="store",type="string",\
            dest="name",help="(REQUIRED)Open-Falcon login user")
    parser.add_option("-p","--password",action="store",type="string",\
            dest="password",help="(REQUIRED)Open-Falcon login user password")
    parser.add_option("-s","--server",action="store",type="string",\
            dest="server",help="(REQUIRED)Open Falcon server")
    parser.add_option("-P","--port",action="store",type="string",\
            dest="port",help="(REQUIRED)api port")
    parser.add_option("--slave",action="store",type="string",\
            dest="mesos",default="http://127.0.0.1:8080/v2/apps",help="(REQUIRED)mesos slave")
    parser.add_option("--consul",action="store",type="string",\
            dest="consul",default="http://127.0.0.1:8500/v1/catalog/service",help="(REQUIRED)consul agent")
    options, args = parser.parse_args()
    if not options.server:
        options.server = raw_input("server http:")
    if not options.name:
        options.name = raw_input("username:")
    if not options.password:
        options.password = getpass.getpass()
    if not options.api:
        options.method = raw_input("api:")
    return options,args

if __name__ == "__main__":
    options,args = get_options()
    name = options.name
    password = options.password
    server = options.server
    api = options.api
    mesos = options.mesos
    consul = options.consul
    port = options.port

    response = urllib2.urlopen(mesos)
    apps = json.loads(response.read())
    openfalconapi = Open_Falcon_Api(server,name,password)
    for app in  apps["apps"]:
        response = urllib2.urlopen(consul+app["id"])
        app_info = response.read()
        app_data = json.loads(app_info)
        ip = []
        for i in app_data:
            ip.append(i["Address"])
        ips = "\n".join(set(ip))
        grp_name =  app["id"].lstrip("/")
        group_name = dict()
        group_name["grp_name"] = grp_name
        try:
            stats = eval("openfalconapi."+api+"(group_name,port)")
            try:
                grp_id = json.loads(stats)["msg"].split(":")[1]
                print grp_id
            except:
                print grp_name+" has already existent"
            hosts = {}
            hosts["group_id"] = grp_id
            hosts["hosts"] = ips
            print eval("openfalconapi._host_add(hosts,port)")
        except:
            pass

