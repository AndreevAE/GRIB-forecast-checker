import os

"""
_<дата начала: ггггММддччмм>+<заблаговременность, ч: ччч>H<заблаговременность, мин: мм>M

не ранее 2013-02-24 18-00
не позднее 2013-03-01 06-00
шаг прогноза - 6 часов
мин заблаговременность - 0 часов
макс заблаговременность - 60 часов
шаг заблаговременности - 1 час
"""

class Forecast:
    def __init__(self, year=2013, month=2, day=24, hours=18, minutes=0, lead_hours=0, lead_minutes=0):
        # fulldate format:
        # yyyyMMddhhmm+hhhHmmM
        # 01234567890123456789

        # TODO: CHECK FULLDATE STRING BY REGEX
        self.year = year
        self.month = month
        self.day = day
        self.hours = hours
        self.minutes = minutes

        self.lead_hours = lead_hours
        self.lead_minutes = lead_minutes

    def __repr__(self):
        return "Forecast()"

    def __str__(self):
        return '{:04d}'.format(self.year)       \
            + '{:02d}'.format(self.month)       \
            + '{:02d}'.format(self.day)         \
            + '{:02d}'.format(self.hours)       \
            + '{:02d}'.format(self.minutes)     \
            + '+'                               \
            + '{:03d}'.format(self.lead_hours)  \
            + 'H'                               \
            + '{:02d}'.format(self.lead_minutes)\
            + 'M'                               \

    def parseFromString(self, fulldate):
        self.year = int(fulldate[0:4])
        self.month = int(fulldate[4:6])
        self.day = int(fulldate[6:8])
        self.hours = int(fulldate[8:10])
        self.minutes = int(fulldate[10:12])

        self.lead_hours = int(fulldate[13:16])
        self.lead_minutes = int(fulldate[17:19])

    def debugPrint(self):
        print("self.year", self.year)
        print("self.month", self.month)
        print("self.day", self.day)
        print("self.hours", self.hours)
        print("self.minutes", self.minutes)
        print("self.lead_hours", self.lead_hours)
        print("self.lead_minutes", self.lead_minutes)

class ForecastChecker:
    """
    forecast_step - шаг прогноза
    min_lead - мин заблаговременность
    max_lead - макс заблаговременность
    lead_step - шаг заблаговременности
    """
    def __init__(self, forecast_step, min_lead, max_lead, lead_step):
        self.forecast_step = forecast_step
        self.min_lead = min_lead
        self.max_lead = max_lead
        self.lead_step = lead_step

    def nextForecast(forecast):
        pass


def open_file(filepath):
    print("NOT IMPLEMENT")

def main():
    fullpath = "./dataset"
    file_folder_list = []
    try:
        file_folder_list = os.listdir(fullpath)
    except FileNotFoundError:
        print("File Not Found")
    except Exception as e:
        print(str(e))
    else:
        #print(file_folder_list)
        open_file(file_folder_list[0])
        fulldate = file_folder_list[0].split('_')[2]
        forecast = Forecast()
        forecast.parseFromString(fulldate)
        print(fulldate)
        print(forecast)
        forecast.debugPrint()
        checker = ForecastChecker(6, 0, 60, 1)




if __name__ == "__main__":
    print("Start")
    try:
        main()
    except KeyboardInterrupt:
        print("Stop serving")
    except Exception as e:
        print(str(e))
