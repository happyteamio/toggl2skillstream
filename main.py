import ConfigParser
import datetime
import requests
from pyquery import PyQuery as pq

config = ConfigParser.ConfigParser()
config.read("config.ini")

shost = config.get("DEFAULT", "SHost")
spath = config.get("DEFAULT", "SPath")
susername = config.get("DEFAULT", "SUsername")
spassword = config.get("DEFAULT", "SPassword")

base_url = "https://" + shost + spath
login_url = base_url + "/j_spring_security_check"
timesheets_url = base_url + "/search.timesheet?submit.search=1&status=unsubmitted"

r = requests.get(base_url)
d = pq(r.text)

authenticity_token = d("input[name='authenticity_token']").attr("value")

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": shost,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": base_url,
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}
payload = {
    "authenticity_token": authenticity_token,
    "cmd": "reqLogin",
    "j_username": susername,
    "j_password": spassword,
    "submit.x": "64",
    "submit.y": "21"
}
cookies = dict(JSESSIONID=r.cookies["JSESSIONID"])

r = requests.post(login_url, headers=headers, data=payload, cookies=cookies)

auth_cookies = r.history[0].cookies

print "Login: " + str(r.status_code)
print "Auth cookies"
print auth_cookies

headers = {
    "Host": shost,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": base_url + "/main_frameset.jsp",
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}
cookies = dict(JSESSIONID=auth_cookies["JSESSIONID"])

r = requests.get(timesheets_url, headers=headers, cookies=cookies)

print r.status_code

d = pq(r.text)

date = datetime.datetime.strptime(d(".timecell")[1].text, "%d/%m/%Y")
