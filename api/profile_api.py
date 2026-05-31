import requests
from config import BASE_URL


class ProfileAPI:
    def get_account(self, access_token: str | None = None):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        res = requests.get(
            f"{BASE_URL}/account",
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()

        return res.json()

    def get_player_rating(self, access_token: str | None = None):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

      

        last_response = None

        res = requests.get(
            f"{BASE_URL}/account/player-rating",
            headers=headers,
            timeout=10,
        )

        if res.status_code != 404:
            res.raise_for_status()
            raw = res.json()
            rating = raw.get("data", raw)
            if not isinstance(rating, dict):
                return raw
            return {
                "overallScore": rating.get("overallScore"),
                "averageTechnicalScore": rating.get("averageTechnicalScore"),
                "skillLevel": rating.get("skillLevel"),
                "verifyCount": rating.get("verifyCount"),
                "slug": rating.get("slug"),
            }

        last_response = res

        if last_response is not None:
            last_response.raise_for_status()

        raise RuntimeError("No player-rating endpoint could be resolved.")

    def get_schedule(
        self,
        access_token: str | None = None,
        page: int = 0,
        size: int = 5,
    ):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        res = requests.get(
            f"{BASE_URL}/account/schedule",
            params={"page": page, "size": size},
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()

        raw = res.json()
        data = raw.get("data", raw)
        items = data.get("content") if isinstance(data, dict) else data
        if not isinstance(items, list):
            return raw

        return {
            "schedules": [
                {
                    "name": item.get("name"),
                    "startTime": item.get("startTime"),
                    "endTime": item.get("endTime"),
                    "status": item.get("status"),
                    "slug": item.get("slug"),
                }
                for item in items[:5]
                if isinstance(item, dict)
            ]
        }
    
    def get_nearby_badminton_players(self, access_token=None):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        res = requests.get(
            f"{BASE_URL}/account/nearby-users",
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()
        raw = res.json()

        players = raw.get("data", [])

        slim = [
            {
                "id": p.get("id"),
                "fullname": p.get("fullName"),
                "avatar": p.get("avatarUrl"),
                "skillLevel": p.get("skillLevel"),
                "mutualFriends": p.get("mutualFriends"),
                "slug": p.get("slug"),
                "url": f"/profile/{p.get('slug')}" if p.get("slug") else None,
            }
            for p in players
        ]

        return {
            "players": slim,
            "total": len(slim),
        }

