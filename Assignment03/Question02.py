import streamlit as st
import requests

st.set_page_config(page_title="Login + Weather Demo")


def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "logged_out" not in st.session_state:
        st.session_state.logged_out = False

def fake_auth(username, password):
    return username != "" and username == password

def geocode_city(city_name):
    """Use Open-Meteo geocoding API to get lat/lon for a city."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1}
    r = requests.get(url, params=params, timeout=10)
    if r.status_code != 200:
        return None
    data = r.json()
    if "results" not in data or not data["results"]:
        return None
    res = data["results"][0]
    return {
        "name": res.get("name"),
        "country": res.get("country"),
        "lat": res.get("latitude"),
        "lon": res.get("longitude"),
    }

def get_current_weather(lat, lon):
    """Use Open-Meteo current weather API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
        "timezone": "auto",
    }
    r = requests.get(url, params=params, timeout=10)
    if r.status_code != 200:
        return None
    data = r.json()
    return data.get("current")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.logged_out = True

# ---------- UI ----------

init_session()
st.title("Simple Login + Weather App")

if st.session_state.logged_out and not st.session_state.logged_in:
    st.success("Thank you for using the app!")
    st.info("Refresh the page to login again.")
else:
    if not st.session_state.logged_in:
        st.subheader("Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

        if submit:
            if fake_auth(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.logged_out = False
                st.success(f"Login successful. Welcome, {username}!")
            else:
                st.error("Invalid credentials. Hint: username and password must be same.")
    else:
        st.subheader(f"Weather Page (User: {st.session_state.username})")

        city = st.text_input("Enter city name")

        if st.button("Get Weather"):
            if city.strip() == "":
                st.warning("Please enter a city name.")
            else:
                loc = geocode_city(city)
                if not loc:
                    st.error("City not found. Try another name.")
                else:
                    weather = get_current_weather(loc["lat"], loc["lon"])
                    if not weather:
                        st.error("Could not fetch weather data.")
                    else:
                        st.success(
                            f"Current weather in {loc['name']}, {loc['country']} "
                            f"(lat: {loc['lat']}, lon: {loc['lon']})"
                        )
                        st.write(f"Temperature: {weather.get('temperature_2m')} °C")
                        st.write(f"Humidity: {weather.get('relative_humidity_2m')} %")
                        st.write(f"Wind speed: {weather.get('wind_speed_10m')} m/s")

        if st.button("Logout"):
            logout()
            st.rerun()

           