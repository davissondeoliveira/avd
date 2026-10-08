"""Entry point for the AVD Python CLI."""

from .cli import parse_args


def main():
    """Entry point for the AVD Python CLI."""
    args = parse_args()
    args.callback(args)


if __name__ == "__main__":
    main()
