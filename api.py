import base64
import json
import requests


class BasicAuthToken(requests.auth.AuthBase):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __call__(self, r):
        authstr = "Basic " + base64.b64encode(
            bytes(self.key + ":" + self.value, "utf-8")
        ).decode("utf-8")
        r.headers["Authorization"] = authstr
        return r


class KomootApi:
    def __init__(self):
        self.user_id = ""
        self.token = ""

    def __build_header(self):
        if self.user_id != "" and self.token != "":
            return {
                "Authorization": "Basic {0}".format(
                    base64.b64encode(
                        bytes(self.user_id + ":" + self.token, "utf-8")
                    ).decode()
                )
            }
        return {}

    @staticmethod
    def __send_request(url, auth, critical=True):
        r = requests.get(url, auth=auth)
        if r.status_code != 200:
            print("Error " + str(r.status_code) + ": " + str(r.json()))
            if critical:
                exit(1)
        return r

    def login(self, email, password):
        print("Logging in...")

        r = self.__send_request(
            "https://api.komoot.de/v006/account/email/" + email + "/",
            BasicAuthToken(email, password),
        )

        self.user_id = r.json()["username"]
        self.token = r.json()["password"]

        print("Logged in as '" + r.json()["user"]["displayname"] + "'")

    def fetch_tours(self, tourType="all", silent=False):
        if not silent:
            print("Fetching tours of user '" + self.user_id + "'...")

        r = self.__send_request(
            "https://api.komoot.de/v007/users/"
            + self.user_id
            + "/tours/?limit=300&format=coordinate_array",
            BasicAuthToken(self.user_id, self.token),
        )

        results = {}
        tours = r.json()["_embedded"]["tours"]
        with open("result.json", "w") as f:
            json.dump(tours, f)
        for tour in tours:
            if tourType != "all" and tourType != tour["type"]:
                continue
            results[tour["id"]] = (
                tour["name"]
                + " ("
                + tour["sport"]
                + "; "
                + str(int(tour["distance"]) / 1000.0)
                + "km; "
                + tour["type"]
                + ")"
            )

        return results

    def fetch_tour(self, tour_id):
        print("Fetching tour '" + tour_id + "'...")

        r = self.__send_request(
            "https://api.komoot.de/v007/tours/"
            + tour_id
            + "?_embedded=coordinates,way_types,"
            "surfaces,directions,participants,"
            "timeline&directions=v2&fields"
            "=timeline&format=coordinate_array"
            "&timeline_highlights_fields=tips,"
            "recommenders",
            BasicAuthToken(self.user_id, self.token),
        )

        return r.json()

    def fetch_highlight_tips(self, highlight_id):
        print("Fetching highlight '" + highlight_id + "'...")

        r = self.__send_request(
            "https://api.komoot.de/v007/highlights/" + highlight_id + "/tips/",
            BasicAuthToken(self.user_id, self.token),
            critical=False,
        )

        return r.json()
