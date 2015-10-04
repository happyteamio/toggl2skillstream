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

d = pq(r.text)

timesheet_url = base_url

for tr in d(".oddrow, .evenrow").items():
    timecell_value = tr(".timecell").text()

    try:
        date = datetime.datetime.strptime(timecell_value, "%d/%m/%Y").date()
    except ValueError:
        date = None
        print "WARNING: Couldn't parse: " + timecell_value

    if date <> None:
        timespan = (date - datetime.date.today()).days

        if timespan >= 0 and timespan <= 6:
            timesheet_path = tr("a").attr("href")
            timesheet_url = timesheet_url + "/" + timesheet_path

headers = {
    "Host": shost,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": timesheets_url,
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}
cookies = dict(JSESSIONID=auth_cookies["JSESSIONID"])

r = requests.get(timesheet_url, headers=headers, cookies=cookies)

d = pq(r.text)

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": shost,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": timesheet_url,
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}
cookies = dict(JSESSIONID=auth_cookies["JSESSIONID"])

payload = { }

for formElement in d("#tform input").items():
    value = ""

    if formElement.attr("value") <> None:
        value = formElement.attr("value")

    payload[formElement.attr("name")] = value

for formElement in d("#tform select").items():
    value = ""

    if formElement("option:selected").attr("value") <> None:
        value = formElement("option:selected").attr("value")
    else:
        value = formElement("option:eq(0)").attr("value")

    payload[formElement.attr("name")] = value

url = base_url + "/" + d("#tform").attr("action")

payload = {
    "costId1": "",
    "costId2": "",
    "costId3": "",
    "date_format": "dd/MM/yyyy",
    "cvId": "53782",
    "friBreakHour": "--",
    "friBreakMinute": "--",
    "friEndHour": "5",
    "friEndMinute": "0",
    "friHour": "4:00",
    "friLeave": "0.0",
    "friLeaveType": "1",
    "friShiftId": "",
    "friShiftNotes": "",
    "friStartHour": "1",
    "friStartMinute": "0",
    "immediateRelease": "N",
    "jobId": "2133",
    "lastTimesheet": "N",
    "layerId": "",
    "monBreakHour": "--",
    "monBreakMinute": "--",
    "monEndHour": "--",
    "monEndMinute": "--",
    "monHour": "",
    "monLeave": "0.0",
    "monLeaveType": "1",
    "monShiftId": "",
    "monShiftNotes": "",
    "monStartHour": "--",
    "monStartMinute": "--",
    "newLayer": "false",
    "overdayfri": "false",
    "overdaymon": "false",
    "overdaysat": "false",
    "overdaysun": "false",
    "overdaythu": "false",
    "overdaytue": "false",
    "overdaywed": "false",
    "publicHolidayfri": "false",
    "publicHolidaymon": "false",
    "publicHolidaysat": "false",
    "publicHolidaysun": "false",
    "publicHolidaythu": "false",
    "publicHolidaytue": "false",
    "publicHolidaywed": "false",
    "rateCode1": "1",
    "rateCode2": "-1",
    "rateCode3": "-1",
    "requestWeekEnd": "04/10/2015",
    "satBreakHour": "--",
    "satBreakMinute": "--",
    "satEndHour": "--",
    "satEndMinute": "--",
    "satHour": "",
    "satLeave": "0.0",
    "satLeaveType": "1",
    "satShiftId": "",
    "satShiftNotes": "",
    "satStartHour": "--",
    "satStartMinute": "--",
    "submit.update": "update timesheet",
    "sunBreakHour": "--",
    "sunBreakMinute": "--",
    "sunEndHour": "--",
    "sunEndMinute": "--",
    "sunHour": "",
    "sunLeave": "0.0",
    "sunLeaveType": "1",
    "sunShiftId": "",
    "sunShiftNotes": "",
    "sunStartHour": "--",
    "sunStartMinute": "--",
    "thuBreakHour": "--",
    "thuBreakMinute": "--",
    "thuEndHour": "--",
    "thuEndMinute": "--",
    "thuHour": "",
    "thuLeave": "0.0",
    "thuLeaveType": "1",
    "thuShiftId": "",
    "thuShiftNotes": "",
    "thuStartHour": "--",
    "thuStartMinute": "--",
    "toManager": "false",
    "totalHour": "4:00",
    "totalLeave": "",
    "tueBreakHour": "--",
    "tueBreakMinute": "--",
    "tueEndHour": "--",
    "tueEndMinute": "--",
    "tueHour": "",
    "tueLeave": "0.0",
    "tueLeaveType": "1",
    "tueShiftId": "",
    "tueShiftNotes": "",
    "tueStartHour": "--",
    "tueStartMinute": "--",
    "units1": "4.00",
    "units2": "",
    "units3": "",
    "wedBreakHour": "--",
    "wedBreakMinute": "--",
    "wedEndHour": "--",
    "wedEndMinute": "--",
    "wedHour": "",
    "wedLeave": "0.0",
    "wedLeaveType": "1",
    "wedShiftId": "",
    "wedShiftNotes": "",
    "wedStartHour": "--",
    "wedStartMinute": "--"
}

r = requests.post(url, headers=headers, data=payload, cookies=cookies)

print r.status_code
