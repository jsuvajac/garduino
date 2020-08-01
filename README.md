# Garduino
This is an automated plant watering solutinon for my backyard garden.
Since the pressure from the hose valve in my backyard is not sufficient to adequatly watery my plants, I divided
the plants int 2 watering groups, each corresponding to a solenoid valve

              +-->  solenoid 1  -->  plant group 1
    valve  ---|
              +-->  solenoid 2  -->  plant group 2

### `Circuit`
It consists of a micorcontroller that controls 2 solenoid valves. 
Since the solenoids requre 12V and the boar can only accept 5V - 10V, I opted for using a buck converter for stepping down the voltager for the MCU and the relay for controlling the relays with 3.3V digital lines from the MCU.


### `Microcontroller`
The micorcontroller has a ESP8266 wifi card and runs a REST server on my local network that allows for remote toggling of GPIO pins over HTTP.

### `REST server`
The goal of the server is to just create an endpoint for toggling the GPIO pins. In this way, the timing for the watering, weather lookup and scheduling is offloaded to the client.

#### endpoints

    POST -> sets up a GPIO pin for state updating (enables in/out for that GPIO)
    PUT  -> sets the state of the GPIO pin (on/off)
    GET  -> returns state json ob

#### example of state on the server

    {
        'id': 2,
        'gpio': 5,
        'status': 1
    }

### `Watering Script`
Turns on one relay at a time and keeps it open for a provided lengthe of time

Currently run daily through a cron job on a home server

#### Example output

    getting weather...
    weather api response:  200 OK
    current conditions:
    Clouds
    Not raining: watering...
    server_state:  200 OK {'id': 2, 'gpio': 5, 'status': 1}
    watering solenoid 1...
    setting pin 16 (201 Created)
    updating pin 16 state -> 0 (200 OK)
    updating pin 16 state -> 1 (200 OK)
    server_state:  200 OK {'id': 1, 'gpio': 16, 'status': 1}
    watering solenoid 2...
    setting pin 5 (201 Created)
    updating pin 5 state -> 0 (200 OK)
    updating pin 5 state -> 1 (200 OK)
    server_state:  200 OK {'id': 2, 'gpio': 5, 'status': 1}

### `Future work: a loose todo`
- Looking into MQTT
- Other ESP projects since I got 5 more of them :D
- moisture/ temeperature sensing
- stats collection / db
- dashboard
- doorbell notifications