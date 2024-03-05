import requests

from bs4 import BeautifulSoup
from tabulate import tabulate
from datetime import datetime

current_year = str(datetime.now().year)

def ampm_to_24(time_str):
    return datetime.strptime(time_str, "%I:%M%p").strftime("%H:%M")

def fetch_forex_factory_economic_calendar():
    url = "https://www.forexfactory.com/calendar.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    #print(f"{response.status_code} 🏁")

    if response.status_code == 200:
        days_list = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        months_numbers = {
            'Jan': "01",
            'Feb': "02",
            'Mar': "03",
            'Apr': "04",
            'May': "05",
            'Jun': "06",
            'Jul': "07",
            'Aug': "08",
            'Sep': "09",
            'Oct': "10",
            'Nov': "11",
            'Dec': "12"
        }
        soup = BeautifulSoup(response.content, "html.parser")
        event_rows = soup.find_all("tr", class_="calendar__row")
        calendar_data = []
        pre_date = ""
        #print(event_rows)
        for row in event_rows:
            try:
                # Extract data from the row
                try:
                    date = row.find("span", class_="date").text.strip()
                    for day in days_list:
                        if day in date:
                            date = date.replace(f"{day} ", "")
                    for month in months_list:
                        if month in date:
                            date = date = date.replace(f"{month} ", "")
                            if int(date) < 10:
                                date = "0" + date
                            date = current_year + "." + months_numbers[month]+"."+date
                    pre_date = date
                except Exception as e:
                    date = pre_date
                time = ampm_to_24(row.find("td", class_="calendar__time").text.strip())
                if time != "":
                    pre_time = time
                elif time == "":
                    time = pre_time
                datetime = date + " " + time
                currency = row.find("td", class_="calendar__currency").text.strip()
                impact = row.find("td", class_="calendar__impact").find("span")["class"][1]
                if impact == "icon--ff-impact-yel":
                    impact = "🟡"
                elif impact == "icon--ff-impact-red":
                    impact = "🔴"
                elif impact == "icon--ff-impact-ora":
                    impact = "🟠"
                actual = row.find("td", class_="calendar__actual").text.strip()
                description = row.find("td", class_="calendar__event").text.strip()
                forecast = row.find("td", class_="calendar__forecast").text.strip()
                previous = row.find("td", class_="calendar__previous").text.strip()

                calendar_data.append(
                    {
                        "datetime": datetime,
                        "currency": currency,
                        "impact": impact,
                        "description": description,
                        "actual": actual,
                        "forecast": forecast,
                        "previous": previous,
                    }
                )
            except Exception as e:
                #print('Error ❌ ' + str(e ) + ' ' + str(row))
                pass

        return calendar_data
    else:
        print("Failed to fetch data from Forex Factory.")
        return None

#data = fetch_forex_factory_economic_calendar()
#print(data)
#for row in data:
#    print(f"{row['impact']} | {row['date']} | {row['time']} | {row['currency']} | {row['description']} | {row['actual']} | {row['forecast']} | {row['previous']}")

#print(tabulate(data, headers="keys", tablefmt="pretty"))