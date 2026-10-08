"""
CLI for the AVD package.
"""

from argparse import ArgumentParser
from pathlib import Path

from .workflow import avd_workflow as workflow


def parse_args(cmd=None):
    """
    Parse command line arguments.
    """

    parser = ArgumentParser(
        prog="avd",
        usage="avd start [options]",
        description="Connect to AVD using xfreerdp on Ubuntu.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_subcmd_start_parser(subparsers)

    return parser.parse_args(cmd)


def add_subcmd_start_parser(subparsers):
    """
    Add a start subcommand parser.
    """

    parser = subparsers.add_parser(
        "start",
        help="Starts the AVD connection",
    )

    parser.add_argument(
        "-l",
        "--location",
        type=str,
        default="Army Desktop.rdpw",
        help="""Path to the location of the AVD connection file.
        Default is 'Army Desktop.rdpw'.
        Example: /home/usr/Army Desktop.rdpw""",
    )

    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="""Username for the AVD connection. Should be your army.mil email address.""",
    )

    parser.set_defaults(callback=subcmd_start_callback)


def subcmd_start_callback(args):
    """
    Callback to unpack args and initiate the workflow.
    """
    _check_paths(args.location, args.username)
    workflow(args.location, args.username)


def _check_paths(location: str, username: str):
    """
    Validate location and username inputs.
    Ensures location exists and username is provided.
    """

    if not Path(location).exists():
        raise FileNotFoundError("Location path does not exist.")

    if not username:
        raise ValueError("Username must be provided.")

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    args.callback(args)
