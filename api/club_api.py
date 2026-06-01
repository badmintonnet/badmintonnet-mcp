import requests
from config import BASE_URL


class ClubAPI:
    def _slim_club(self, club: dict):
        facility = club.get("facility") or {}
        slug = club.get("slug")
        return {
            "id": club.get("id"),
            "name": club.get("name"),
            "slug": slug,
            "url": f"/clubs/{slug}" if slug else None,
            "location": (
                club.get("location")
                or facility.get("location")
                or facility.get("address")
            ),
            "facilityName": facility.get("name"),
            "memberCount": club.get("memberCount"),
            "maxMembers": club.get("maxMembers"),
            "totalEvent": club.get("totalEvent"),
            "tags": club.get("tags"),
            "status": club.get("status"),
            "distanceKm": club.get("distanceKm"),
        }

    def _extract_items(self, raw: dict):
        data = raw.get("data", raw)
        if isinstance(data, dict):
            items = data.get("content", [])
        else:
            items = data
        return items if isinstance(items, list) else []

    def get_public_clubs(
        self,
        access_token: str | None = None,
        search=None,
        province=None,
        ward=None,
        selectedLevels=None,
        facilityNames=None,
        reputationSort=None,
    ):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        params = {
            "page": 0,
            "size": 5,
        }

        if search:
            params["search"] = search
        if province:
            params["province"] = province
        if ward:
            params["ward"] = ward
        if selectedLevels:
            params["selectedLevels"] = selectedLevels
        if facilityNames:
            params["facilityNames"] = facilityNames
        if reputationSort:
            params["reputationSort"] = reputationSort

        res = requests.get(
            f"{BASE_URL}/clubs/all_public",
            params=params,
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()
        raw = res.json()
        data = raw.get("data", {})
        clubs = self._extract_items(raw)

        return {
            "clubs": [self._slim_club(c) for c in clubs[:5]],
            "page": data.get("page"),
            "totalPages": data.get("totalPages"),
            "last": data.get("last"),
        }

    def join_club(
        self,
        access_token: str,
        club_id: str,
    ):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        payload = {
            "notification": "Toi muon tham gia cau lac bo cua ban tren BadmintonNet!",
        }

        res = requests.post(
            f"{BASE_URL}/clubs/{club_id}/join",
            json=payload,
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()

        return res.json()

    def get_nearby_badminton_clubs(
        self,
        access_token: str,
    ):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        res = requests.get(
            f"{BASE_URL}/clubs/nearby",
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()
        clubs = self._extract_items(res.json())
        return {
            "clubs": [self._slim_club(c) for c in clubs[:3]],
            "total": len(clubs),
            "note": "Only first 3 nearby clubs are returned to keep AI context small.",
        }
