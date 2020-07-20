import sys

id_file = "id.txt"
files = ["rest/rest.ino", "server/server.ino"]

def main(args):
    if (args[1] == "remove"):
        for name in files:
            clean_cred(name)
    elif (args[1] == "add"):
        for name in files:
            write_cred(name)

def clean_cred(server_file):
    with open(server_file) as f:
        lines = f.readlines()

    with open(server_file, "w") as f:
        for line in lines:
            if ("const char* wifi_ssid" in line):
                line = line.split("\"")
                line = line[0] + "\"\"" + line[2]

            elif ("const char* wifi_passwd" in line):
                line = line.split("\"")
                line = line[0] + "\"\"" + line[2]

            f.write(line)

def write_cred(server_file):
    with open(id_file) as f:
        ssid = f.readline().rstrip()
        password = f.readline().rstrip()

    with open(server_file) as f:
        lines = f.readlines()

    with open(server_file, "w") as f:
        for line in lines:
            if ("const char* wifi_ssid" in line):
                line = line.split("\"")
                line = line[0] + '"' + ssid + '"' +line[2]
                
            elif ("const char* wifi_passwd" in line):
                line = line.split("\"")
                line = line[0] + '"' + password + '"' +line[2]

            f.write(line)


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print(f"Usage: \n\tremove \n\tadd")
        sys.exit(0)

    main(sys.argv)
