from urllib import request
import time

f = open("link.log", 'r')
url = f.read()
url = url.splitlines()

for u in url:
    t = time.localtime()
    current_time = time.strftime("%H_%M_%S", t)
    request.urlretrieve(u, "Images/" + current_time + ".jpg")
