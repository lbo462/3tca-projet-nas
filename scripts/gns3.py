import gns3fy
from telnetlib import Telnet
from time import sleep


def main():
    gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
    lab = gns3fy.Project(name="API TEST", connector=gns3_server)
    lab.get()
    lab.open()

    with Telnet('localhost', 5000) as tn:
        tn.write(b"conf t")
        sleep(1)


if __name__ == "__main__":
    main()
