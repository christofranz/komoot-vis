import json

from api import KomootApi

MAIL = "<your-komoot-mail>"
PWD = "<your-komoot-passsword>"


def main():

    # set up api and login
    api = KomootApi()
    api.login(MAIL, PWD)

    # get all tours and fetch details for each
    tours = api.fetch_tours()
    for t in tours:
        tour_details = api.fetch_tour(str(t))
        # store details
        with open(f"data/{t}.json", "w") as f:
            json.dump(tour_details, f)


if __name__ == "__main__":
    main()
