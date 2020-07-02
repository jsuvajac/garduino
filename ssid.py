import sys

id_file = "id.txt"
server_file = "server.ino"

def main(args):
    if (args[1] == "remove"):
        clean_cred()
    elif (args[1] == "add"):
        write_cred()

def clean_cred():
    with open(server_file) as f:
        lines = f.readlines()

    with open(server_file, "w") as f:
        for line in lines:
            if ("const char* ssid" in line):
                line = line.split("\"")
                line = line[0] + "\"\"" + line[2]

            elif ("const char* password" in line):
                line = line.split("\"")
                line = line[0] + "\"\"" + line[2]

            f.write(line)

def write_cred():
    with open(id_file) as f:
        ssid = f.readline().rstrip()
        password = f.readline().rstrip()

    with open(server_file) as f:
        lines = f.readlines()

    with open(server_file, "w") as f:
        for line in lines:
            if ("const char* ssid" in line):
                line = line.split("\"")
                line = line[0] + '"' + ssid + '"' +line[2]
                
            elif ("const char* password" in line):
                line = line.split("\"")
                line = line[0] + '"' + password + '"' +line[2]

            f.write(line)


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print(f"Usage: \n\tremove \n\tadd")
        sys.exit(0)

    main(sys.argv)
