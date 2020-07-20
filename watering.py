import http.client
import json
import time

WATERING_TIME = 3 # in sec

SOLENOID_1 = 16
SOLENOID_2 = 5

ESP_IP = "192.168.0.40"

def set_response(id, gpio, status):
    return {
        'id': id,
        'gpio': gpio,
        'status': status,
    }

def get_status(conn):
    conn.request("GET", "/leds")
    res = conn.getresponse()
    binary = res.read()
    json_resp = json.loads(binary.decode())
    print("individual: ", res.status, res.reason, json_resp)

def post(conn, id, gpio, status):
    conn.request("POST", "/leds", json.dumps(set_response(id, gpio, status)))
    r2 = conn.getresponse()
    print(r2.status, r2.reason)

def put(conn, id, gpio, status):
    conn.request("PUT", "/leds", json.dumps(set_response(id, gpio, status)))
    r2 = conn.getresponse()
    print(r2.status, r2.reason)

def trigger_solenoid(id, solenoid):
    post(conn, id, solenoid, 0)
    put(conn, id, solenoid, 0)
    time.sleep(WATERING_TIME)
    put(conn, id, solenoid, 1)


if __name__ == "__main__":
    conn = http.client.HTTPConnection(ESP_IP)
    get_status(conn)

    trigger_solenoid(1, SOLENOID_1)
    trigger_solenoid(2, SOLENOID_2)
