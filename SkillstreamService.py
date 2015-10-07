import sys
import ConfigParser
from pyquery import PyQuery as pq

class SkillstreamService:

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("config.ini")

        self.host = config.get("DEFAULT", "SHost")
        self.path = config.get("DEFAULT", "SPath")
        self.username = config.get("DEFAULT", "SUsername")
        self.password = config.get("DEFAULT", "SPassword")

        self.base_url = "https://" + self.host + self.path

    def authorize(func):
        def inner(*args, **kwargs):
            print "Logging in.."

            print args[0].get_header()

            try:
                func(*args, **kwargs)
            except:
                print sys.exc_info()[0]
            finally:
                print "Logging out.."

        return inner

    @authorize
    def report_hours(self, date, hours, minutes):

        print "Reporting hours.."

    def get_header(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
