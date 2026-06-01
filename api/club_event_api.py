import requests
from config import BASE_URL


def _normalize_local_datetime(value: str, is_end: bool = False) -> str:
    """Convert YYYY-MM-DD to ISO LocalDateTime expected by backend."""
    if "T" in value:
        return value

    date_part = value.strip()

    if len(date_part) == 10 and date_part[4] == "-" and date_part[7] == "-":
        return f"{date_part}T23:59:59" if is_end else f"{date_part}T00:00:00"

    return value


class ClubEventAPI:
    def _slim_event(self, event: dict):
        facility = event.get("facility") or {}
        slug = event.get("slug")
        return {
            "id": event.get("id"),
            "title": event.get("title"),
            "slug": slug,
            "url": f"/events/{slug}" if slug else None,
            "location": (
                event.get("location")
                or facility.get("location")
                or facility.get("address")
            ),
            "facilityName": facility.get("name"),
            "startTime": event.get("startTime"),
            "endTime": event.get("endTime"),
            "fee": event.get("fee"),
            "totalSlot": event.get("totalMember"),
            "joinedSlot": event.get("joinedMember"),
            "clubName": event.get("nameClub") or event.get("clubName"),
            "categories": event.get("categories"),
            "status": event.get("status"),
            "distanceKm": event.get("distanceKm"),
        }

    def _extract_items(self, raw: dict):
        data = raw.get("data", raw)
        if isinstance(data, dict):
            items = data.get("content", [])
        else:
            items = data
        return items if isinstance(items, list) else []

    def get_public_club_events(
        self,
        access_token: str | None = None,
        page: int = 0,
        size: int = 5,
        search: str | None = None,
        province: str | None = None,
        ward: str | None = None,
        quickTimeFilter: str | None = None,
        isFree: bool | None = None,
        minFee: float | None = None,
        maxFee: float | None = None,
        startDate: str | None = None,
        endDate: str | None = None,
        advancedFilter: dict | None = None,
    ):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        params = {
            "page": page,
            "size": min(size, 5),
        }

        if search:
            params["search"] = search
        if province:
            params["province"] = province
        if ward:
            params["ward"] = ward
        if quickTimeFilter:
            params["quickTimeFilter"] = quickTimeFilter
        if isFree is not None:
            params["isFree"] = isFree
        if minFee is not None:
            params["minFee"] = minFee
        if maxFee is not None:
            params["maxFee"] = maxFee
        if startDate:
            params["startDate"] = _normalize_local_datetime(startDate)
        if endDate:
            params["endDate"] = _normalize_local_datetime(endDate, is_end=True)

        res = requests.post(
            f"{BASE_URL}/club-event/all/public",
            params=params,
            json=advancedFilter if advancedFilter is not None else None,
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()
        raw = res.json()
        data = raw.get("data", {})
        events = self._extract_items(raw)

        return {
            "events": [self._slim_event(e) for e in events[:5]],
            "page": data.get("page"),
            "totalPages": data.get("totalPages"),
            "last": data.get("last"),
        }

    def join_event(
        self,
        access_token: str,
        event_id: str,
    ):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        res = requests.post(
            f"{BASE_URL}/club-event/join/{event_id}",
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()

        return res.json()

    def get_nearby_club_events(
        self,
        access_token: str,
    ):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        res = requests.get(
            f"{BASE_URL}/club-event/nearby",
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()
        events = self._extract_items(res.json())
        return {
            "events": [self._slim_event(e) for e in events[:3]],
            "total": len(events),
            "note": "Only first 3 nearby events are returned to keep AI context small.",
        }
