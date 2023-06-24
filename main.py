import requests
from datetime import datetime
import smtplib

MY_LAT = 51.50
MY_LNG = -0.1277
EMAIL = "OtisTestEmail@gmail.com"
PASSWORD = "1234qwer"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    longitute = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    if (MY_LAT - 5) <= latitude <= (MY_LAT + 5) and (MY_LNG - 5) <= longitute <= (MY_LNG + 5):
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()


    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    timeNow = datetime.now().hour

    if timeNow >= sunset or timeNow <= sunrise:
        return True


if is_iss_overhead() and is_night():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(EMAIL, PASSWORD)
    connection.sendmail(
        from_addr=EMAIL,
        to_addrs=EMAIL,
        msg="Subject:Look Up\n\nThe ISS is above you in the sky"
    )
