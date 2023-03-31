import gns3fy

from backbone import Backbone
from gns3 import GNS3Config

JSON_FILE_NAME = "bb_config.json"

HOST = "localhost"
PORT = 3080
PROJECT_NAME = "ProjetNAS"


def main():
    # Connect to GNS3 server
    gns3_server = gns3fy.Gns3Connector(f"http://{HOST}:{PORT}")

    # Retrieve and open project
    lab = gns3fy.Project(name=PROJECT_NAME, connector=gns3_server)
    lab.get()
    lab.open()

    # Create GNS3 config
    gns3_config = GNS3Config(HOST, lab.nodes)

    # Create backbone
    backbone = Backbone(JSON_FILE_NAME, gns3_config)

    # Get a preview of what is going to happen
    print(backbone.get_all_configs())

    # Configure backbone ON GNS3
    # backbone.write_configs()


if __name__ == "__main__":
    main()
