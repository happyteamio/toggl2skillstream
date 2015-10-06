import sys

class SkillstreamService:

    def authorize(func):
        def inner(*args, **kwargs):
            print "Logging in.."

            try:
                func(*args, **kwargs)
            except:
                print sys.exc_info()[0]
            finally:
                print "Logging out.."

        return inner

    @authorize
    def report_hours(self, date, hours, minutes):
        raise NotImplementedError
