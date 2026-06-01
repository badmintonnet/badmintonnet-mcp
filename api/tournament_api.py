import requests
from config import BASE_URL


class TournamentAPI:
    def _slim_tournament(self, tournament: dict):
        facility = tournament.get("facility") or {}
        slug = tournament.get("slug")
        return {
            "id": tournament.get("id"),
            "name": tournament.get("name"),
            "slug": slug,
            "url": f"/tournaments/{slug}" if slug else None,
            "location": (
                tournament.get("location")
                or facility.get("location")
                or facility.get("address")
            ),
            "facilityName": facility.get("name"),
            "startDate": tournament.get("startDate"),
            "endDate": tournament.get("endDate"),
            "registrationStartDate": tournament.get("registrationStartDate"),
            "registrationEndDate": tournament.get("registrationEndDate"),
            "status": tournament.get("status"),
            "participationType": tournament.get("participationType"),
            "fee": tournament.get("fee") or tournament.get("clubRegistrationFee"),
            "distanceKm": tournament.get("distanceKm"),
        }

    def _extract_items(self, raw: dict):
        data = raw.get("data", raw)
        if isinstance(data, dict):
            items = data.get("content", [])
        else:
            items = data
        return items if isinstance(items, list) else []

    def get_my_club_tournaments(
        self,
        access_token: str | None = None,
        page: int = 0,
        size: int = 5,
        organizationDateFrom: str | None = None,
        organizationDateTo: str | None = None,
    ):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        params = {
            "page": page,
            "size": min(size, 5),
        }

        if organizationDateFrom:
            params["organizationDateFrom"] = organizationDateFrom

        if organizationDateTo:
            params["organizationDateTo"] = organizationDateTo

        res = requests.get(
            f"{BASE_URL}/tournaments",
            params=params,
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()
        raw = res.json()
        data = raw.get("data", {})
        tournaments = self._extract_items(raw)

        return {
            "tournaments": [self._slim_tournament(t) for t in tournaments[:5]],
            "page": data.get("page"),
            "totalPages": data.get("totalPages"),
        }

    def get_nearby_badminton_tournaments(
        self,
        access_token: str | None = None,
    ):
        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        res = requests.get(
            f"{BASE_URL}/tournaments/nearby",
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()
        tournaments = self._extract_items(res.json())
        return {
            "tournaments": [self._slim_tournament(t) for t in tournaments[:3]],
            "total": len(tournaments),
            "note": "Only first 3 nearby tournaments are returned to keep AI context small.",
        }
