import requests

api_key="b5dfdb6ce17492174919c6ae018d9ec3"
city = input("Enter city: ")
 
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=b5dfdb6ce17492174919c6ae018d9ec3&units=metric"
response = requests.get(url)
print("status:", response.status_code)
weather = response.json()
# print(weather)

print("Temperature: ", weather["main"]["temp"])
print("Humidity: ", weather["main"]["humidity"])
print("Wind Speed: ", weather["wind"]["speed"])

if __name__ == "__main__":
    pass
