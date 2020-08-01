import http.client
import json
import time
import sys
import argparse
from pprint import pprint

WATERING_TIME = 3 # in sec

SOLENOID_1 = 16
SOLENOID_2 = 5

API_FILE = "api_keys.txt"

# vars to json obj
def set_response(id, gpio, status):
    return {
        'id': id,
        'gpio': gpio,
        'status': status,
    }

# returns state 
def get_status(conn):
    conn.request("GET", "/leds")
    res = conn.getresponse()
    if res.status != 204:
        binary = res.read()
        json_resp = json.loads(binary.decode())
        print("server_state: ", res.status, res.reason, json_resp)
    else:
        print("server_state: No previous state")

# set gpio pin for being updatable
def post(conn, id, gpio, status):
    conn.request("POST", "/leds", json.dumps(set_response(id, gpio, status)))
    r2 = conn.getresponse()
    print("setting pin {} ({} {})".format(gpio, r2.status, r2.reason))

# set gpio pin state
def put(conn, id, gpio, status):
    conn.request("PUT", "/leds", json.dumps(set_response(id, gpio, status)))
    r2 = conn.getresponse()
    print("updating pin {} state -> {} ({} {})"
        .format(gpio, status, r2.status, r2.reason))

# water solenoid for a duration
def trigger_solenoid(conn, id, solenoid):
    post(conn, id, solenoid, 0)
    put(conn, id, solenoid, 0)
    time.sleep(WATERING_TIME)
    put(conn, id, solenoid, 1)
    get_status(conn)

# request current weather from open weather api
def get_weather(api_file, lat, lon):
    with open(api_file) as f:
        api_key = f.readline().rstrip()
    
    print("getting weather...") 
    con = http.client.HTTPConnection("api.openweathermap.org", 80)
    con.request('GET',
        "/data/2.5/onecall?"
        "lat={}&"
        "lon={}&"
        "units=metric&"
        "exclude=minutely,hourly,daily&"
        "appid={}"
        .format(lat, lon, api_key))

    res =  con.getresponse()
    json_resp = json.loads(res.read().decode())
    
    print("weather api response: ", res.status, res.reason)

    return json_resp

# returns true if open weather api claims its raining at the time of execution
def is_raining(weather):
    # more info on conditions:
    # https://openweathermap.org/weather-conditions#How-to-get-icon-URL

    bad_weather = ['Thunderstorm', 'Drizzle', 'Rain', 'Snow']
    print("current conditions:")
    for condition in weather['weather']:
        print(condition['main'])
        if condition['main'] in bad_weather:
            return True

    return False

def main(ip):
    # Guelph coords
    lat = 43.55
    lon = -80.25
    weather = get_weather(API_FILE, lon, lat)

    if is_raining(weather['current']):
        print("Raining: stopping watering...")
        exit(0)
    else:
        print("Not raining: watering...")

    conn = http.client.HTTPConnection(ip)

    try:
        get_status(conn)
    except ConnectionRefusedError:
        print(f"Connection refused for ip: {ip}")
        exit(1)

    print("watering solenoid 1...")
    trigger_solenoid(conn, 1, SOLENOID_1)

    print("watering solenoid 2...")
    trigger_solenoid(conn, 2, SOLENOID_2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="plant watering client for ESP REST API")
    parser.add_argument("ip", type=str, help="ip of ESP MCU")
    parser.add_argument(
        "-t",
        "--time",
        type=float,
        action='store',
        help="watering time in seconds")

    args = parser.parse_args()

    if args.time and args.time > 0:
        WATERING_TIME = args.time

    if args.ip:
        main(args.ip)
