Open_Faclon_Api
================================================================
Open_Faclon_Api is a python module for working the [open-falcon api](http://docs.openfalcon.apiary.io/).

----------------------------------------------------------------
###examples using:
> 
from core import Open_Falcon_Api
> 
of = Open_Falcon_Api("http://127.0.0.1","user","password")
> 
of.ips(None,1988)
> 
of.page_cpu_usage(None,1988)

###result:
> 
{"msg":"success","data":[""]}
> 
{"msg":"success","data":[["90.5%","9.5%","7.3%","0.0%","2.3%","0.0%","0.0%","0.0%","0.0%","0.0%"]]}

