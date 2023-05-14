import argparse


def get_arg_parser():
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

    parser.add_argument(
        "--dry-run", "-d", action="store_true", help="Don't push anything to devices."
    )

    return parser


APP_ARGS = get_arg_parser().parse_args()
