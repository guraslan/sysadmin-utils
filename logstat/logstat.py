import time
import memcache
from datetime import datetime

# max 500 request/s geldigini varsayiyorum.
sleeptime = 1.0/500
# reportime kadar saniyede bir memcache e yazsin, rcounter limit
reporttime=5.0
rlimit=reporttime/sleeptime 
rcounter = 0 # report counter

def follow(thefile): 
    thefile.seek(0,2)      # Go to the end of the file
    while True:
         line = thefile.readline()
         if not line:
	     if ishourstart():
		break  # a new generator with a new file 
             time.sleep(sleeptime)    # Sleep briefly
	     report()
             continue
         yield line

def report():
   global rcounter
   global statcount
   totalrps = 0
#   print rcounter,rlimit
   if rcounter >= rlimit:  
     for s,v in enumerate(statcount):
         insertMemcache('192.168.34.22_http_' + v, statcount[v]/reporttime)
	 totalrps += statcount[v]
 	 statcount[v] = 0 # zero out after report
     insertMemcache('192.168.34.22_http_' + "total", totalrps/reporttime)
     rcounter = 0
   else:
     rcounter += 1


# parse and count http codes
def count(loglines):
    global statcount
    offset = 8
    for line in loglines:
        sline = line.split()
        try:
                status = sline[offset]
        except IndexError:
                print line
                continue

	if status in statcount.keys():
        	statcount[status] += 1
    
    #for i, v in enumerate(statcount):


def insertMemcache(k, v):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    mc.set(k, v)
    #value = mc.get(k)
    #print k,value
    print k,v


# build next log file name
def findnextlogfile(header, curdir):
    dt = datetime.now() 
    return curdir + header + dt.strftime("-%Y-%m-%d-%H") + ".log"

# hour start hh:00:00 -> hh:00:03 
def ishourstart():
    dt = datetime.now() 
    minute = dt.strftime("%M")
    second = dt.strftime("%S")
	
    if int(minute) == 0 and int(second) <=3: # 3 saniye kacabilir diye bir guven araligi
       return True
    return False


### main ####
global statcount
statcount = {'200':0, '206':0, '301':0, '302':0, '304':0, '404':0, '500':0}

nameheader="access" # sys.argv[1]
cwd="/data/logs/"



while True:
   fn = findnextlogfile(nameheader, cwd)
   print fn
   try:
   	logfile = open(fn)
   except IOError:
	time.sleep(2)	
	logfile = open(fn)
	
   loglines = follow(logfile)
   count(loglines)
   logfile.close()


#for s,v in enumerate(statcount):
#    print v, statcount[v]
