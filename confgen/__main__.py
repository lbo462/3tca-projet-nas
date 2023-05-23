import gns3fy

from .settings import APP_ARGS
from .backbone import Backbone
from .gns3 import GNS3Config


def main():
    # Read args
    path_to_json = APP_ARGS.path_to_json
    project_name = APP_ARGS.name
    host = APP_ARGS.host if APP_ARGS.host else "localhost"
    port = APP_ARGS.port if APP_ARGS.port else 3080

    # Connect to GNS3 server
    addr = f"http://{host}:{port}"  # noqa
    if APP_ARGS.verbose:
        print(f"> Connecting to {addr} ...")
    gns3_server = gns3fy.Gns3Connector(addr)

    # Retrieve and open project
    if APP_ARGS.verbose:
        print(f"> Loading project ...")
    lab = gns3fy.Project(name=project_name, connector=gns3_server)  # noqa
    lab.get()
    lab.open()

    # Create GNS3 config
    gns3_config = GNS3Config(host, lab.nodes)

    # Create backbone
    if APP_ARGS.verbose:
        print(f"> Creating backbone ...")
    backbone = Backbone(path_to_json, gns3_config)

    # Get a preview of what is going to happen
    if APP_ARGS.verbose:
        print("> Configs to send to backbone:")
        print(backbone.get_all_configs())

    # Configure backbone ON GNS3
    print("> Starting writing config to routers ...")
    recap = backbone.write_configs()

    with open("recap.txt", "w") as f:
        f.write(recap)

    print(f"> Configuration written to routers. See `recap.txt`")


if __name__ == "__main__":
    main()
