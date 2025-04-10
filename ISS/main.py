import requests
import datetime as dt
import smtplib
my_email = "EmailAddress"
password = "email _password"
MY_LAT = 6.528017
MY_LNG = 3.338459

iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()     # raising exceptions
iss_data = iss_response.json()     # getting the API data

longitude = float(iss_data['iss_position']['longitude'])
latitude = float(iss_data['iss_position']['latitude'])
iss_position = (longitude, latitude)
print(iss_position)

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
sunrise_day = int(data['results']['sunrise'].split('T')[0].split('-')[2])


lng_difference = abs(longitude-MY_LNG)
lat_difference = abs(latitude-MY_LAT)

day = dt.datetime.now()
date = day.day
current_time = day.time().hour

while True:
    if lat_difference <= 5 and lng_difference <= 5:
        if (date == sunrise_day and current_time >= sunset) or (date > sunrise_day and current_time <= sunrise):
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs=my_email,
                                    msg=f"Subject: ISS is around you bro!! {day}!!!\n\n look up")
