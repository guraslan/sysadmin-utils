import memcache
import sys

if len(sys.argv) < 2:
   print "ZBX_UNSUPPORTED"
   exit(1)

reporttime=5.0
statcount = {'200':0, '206':0, '301':0, '302':0, '304':0, '404':0, '500':0}

def getstats(k):
    mc = memcache.Client(['192.168.34.22:11211'], debug=0)
    value = mc.get(k)
    print value

#for s,v in enumerate(statcount):
#    getstats('192.168.34.22_http_' + v)
code=sys.argv[1]
getstats('192.168.34.22_http_' + code)
    
