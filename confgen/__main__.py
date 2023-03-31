import gns3fy
import argparse

from .backbone import Backbone
from .gns3 import GNS3Config


def main():
    # Retrieve args
    args = get_args()
    path_to_json = args.path_to_json
    project_name = args.name
    host = args.host if args.host else "localhost"
    port = args.port if args.port else 3080
    verbosity = args.verbose

    # Connect to GNS3 server
    gns3_server = gns3fy.Gns3Connector(f"http://{host}:{port}")

    # Retrieve and open project
    lab = gns3fy.Project(name=project_name, connector=gns3_server)
    lab.get()
    lab.open()

    # Create GNS3 config
    gns3_config = GNS3Config(host, lab.nodes)

    # Create backbone
    backbone = Backbone(path_to_json, gns3_config)

    # Get a preview of what is going to happen
    if verbosity:
        print(backbone.get_all_configs())

    # Configure backbone ON GNS3
    print("Starting writing config to routers ...")
    backbone.write_configs()


def get_args():
    """
    Define a custom argument parser and return passed args
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--path_to_json", "-c", required=True, help="Path to the JSON config file."
    )

    parser.add_argument(
        "--host", help="Hostname for the GNS3 server. Default is `localhost`."
    )

    parser.add_argument(
        "--port", "-p", help="Port for the GNS3 server. Default is 3080."
    )

    parser.add_argument("--name", "-n", required=True, help="GNS3 project name.")

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="More verbose output"
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
