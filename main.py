import os
import pupygrib as grib

"""
pip install -r requirements.txt
pupygrib
"""

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
    forecast_step - шаг прогноза в часах
    min_lead - мин заблаговременность в часах
    max_lead - макс заблаговременность в часах
    lead_step - шаг заблаговременности в часах
    """
    def __init__(self, forecast_step, min_lead, max_lead, lead_step):
        self.forecast_step = forecast_step
        self.min_lead = min_lead
        self.max_lead = max_lead
        self.lead_step = lead_step

    def nextForecast(self, forecast):
        # copy forecast to next
        nextForecast = Forecast()
        # TODO: refactor to normal carriers
        nextForecast.lead_hours = (forecast.lead_hours + self.lead_step) % self.max_lead
        delta_hours = int((forecast.lead_hours + self.lead_step) / self.max_lead)
        #print("delta_hours", delta_hours)
        nextForecast.hours = (delta_hours * self.forecast_step) % 24
        delta_days = int((delta_hours * self.forecast_step) / 24)
        #print("delta_days", delta_days)
        nextForecast.day = (forecast.day + delta_days) % 29
        delta_months = int((forecast.day + delta_days) / 29)
        #print("delta_months", delta_months)
        nextForecast.month = int(forecast.month + delta_months) % 13
        delta_years = int((forecast.month + delta_months) / 13)
        #print("delta_years", delta_years)
        nextForecast.year = forecast.year + delta_years
        return nextForecast


def open_file(filepath):
    with open("./dataset/" + filepath, 'rb') as stream:
        try:
            for i, msg in enumerate(grib.read(stream), 1):
                lons, lats = msg.get_coordinates()
                # values = msg.get_values()
                # print("Message {}: {}".format(i, lons.shape))
                # print("Message {}: {:.3f} {}".format(i, values.mean(), lons.shape))
        except Exception as e:
            print(filepath," ", str(e))



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
        file_folder_list.sort()
        # for file in file_folder_list:
        #     print(file)

        # print(file_folder_list)
        # for i, file in enumerate(file_folder_list):
           # print("File ", i)
            # open_file(file)

        open_file(file_folder_list[0])
        fulldate = file_folder_list[0].split('_')[-1]
        print(fulldate)
        forecast = Forecast()
        forecast.parseFromString(fulldate)
        print(forecast)
        # forecast.debugPrint()
        checker = ForecastChecker(6, 0, 60, 1)
        nextForecast = checker.nextForecast(forecast)
        print(nextForecast)
        print(file_folder_list[1].split('_')[-1])




if __name__ == "__main__":
    print("Start")
    try:
        main()
    except KeyboardInterrupt:
        print("Stop program")
    except Exception as e:
        print(str(e))
