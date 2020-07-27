import http.client
import json
import time
import sys

WATERING_TIME = 3 # in sec

SOLENOID_1 = 16
SOLENOID_2 = 5

def set_response(id, gpio, status):
    return {
        'id': id,
        'gpio': gpio,
        'status': status,
    }

def get_status(conn):
    conn.request("GET", "/leds")
    res = conn.getresponse()
    if res.status != 204:
        binary = res.read()
        json_resp = json.loads(binary.decode())
        print("server_state: ", res.status, res.reason, json_resp)
    else:
        print("server_state: No previous state")


def post(conn, id, gpio, status):
    conn.request("POST", "/leds", json.dumps(set_response(id, gpio, status)))
    r2 = conn.getresponse()
    print(r2.status, r2.reason)

def put(conn, id, gpio, status):
    conn.request("PUT", "/leds", json.dumps(set_response(id, gpio, status)))
    r2 = conn.getresponse()
    print(r2.status, r2.reason)

def trigger_solenoid(conn, id, solenoid):
    post(conn, id, solenoid, 0)
    put(conn, id, solenoid, 0)
    time.sleep(WATERING_TIME)
    put(conn, id, solenoid, 1)


def main(ip):
    conn = http.client.HTTPConnection(ip)

    try:
        get_status(conn)
    except ConnectionRefusedError:
        print(f"Connection refused for ip: {ip}")
        exit(1)

    print("watering solenoid 1...")
    trigger_solenoid(conn, 1, SOLENOID_1)
    get_status(conn)

    print("watering solenoid 2...")
    trigger_solenoid(conn, 2, SOLENOID_2)
    get_status(conn)

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(f"Usage: {sys.argv[0]} ip")