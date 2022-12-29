import argparse
import getpass
import json
from api import KomootApi


def main():
    # parse arguments and request pwd input
    parser = argparse.ArgumentParser(description="Query and download your komoot data.")
    parser.add_argument(
        "-m", "--mail", help="E-Mail address for komoot login.", required=True, type=str
    )
    parser.add_argument(
        "-p", "--password", help="Password for komoot login.", required=False, type=str
    )
    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass()

    # set up api and login
    api = KomootApi()
    api.login(args.mail, args.password)

    # get all tours and fetch details for each
    tours = api.fetch_tours()
    for t in tours:
        tour_details = api.fetch_tour(str(t))
        # store details
        with open(f"data/{t}.json", "w") as f:
            json.dump(tour_details, f)


if __name__ == "__main__":
    main()
