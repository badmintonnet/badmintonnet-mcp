import requests
from config import BASE_URL


class RecommendationAPI:
    def get_personalized_recommendations(
        self,
        access_token: str | None = None,
        top: int = 3,
    ):
        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        res = requests.get(
            f"{BASE_URL}/recommendations",
            params={"top": max(1, min(top, 5))},
            headers=headers,
            timeout=15,
        )
        res.raise_for_status()

        raw = res.json()
        data = raw.get("data", raw)

        return {
            "profile": self._slim_profile(data.get("profile") or {}),
            "clubs": self._slim_items(data.get("clubs") or []),
            "events": self._slim_items(data.get("events") or []),
            "tournaments": self._slim_items(data.get("tournaments") or []),
            "generatedAt": data.get("generatedAt"),
        }

    def _slim_profile(self, profile: dict):
        return {
            "fullName": profile.get("fullName"),
            "skillScore": profile.get("skillScore"),
            "skillLevel": profile.get("skillLevel"),
            "hasLocation": profile.get("hasLocation"),
            "favoriteCategories": profile.get("favoriteCategories") or [],
            "preferredTimeSlots": profile.get("preferredTimeSlots") or [],
        }

    def _slim_items(self, items: list[dict]):
        return [self._slim_item(item) for item in items]

    def _slim_item(self, item: dict):
        return {
            "type": item.get("type"),
            "id": item.get("id"),
            "title": item.get("title"),
            "subtitle": item.get("subtitle"),
            "slug": item.get("slug"),
            "url": item.get("detailUrl"),
            "clubName": item.get("clubName"),
            "status": item.get("status"),
            "location": item.get("location"),
            "facilityName": (item.get("facility") or {}).get("name"),
            "score": item.get("score"),
            "distanceKm": item.get("distanceKm"),
            "minLevel": item.get("minLevel"),
            "maxLevel": item.get("maxLevel"),
            "joinedSlots": item.get("joinedSlots"),
            "totalSlots": item.get("totalSlots"),
            "fee": item.get("fee"),
            "startTime": item.get("startTime"),
            "endTime": item.get("endTime"),
            "registrationEndDate": item.get("registrationEndDate"),
            "categories": item.get("categories") or [],
            "tags": item.get("tags") or [],
            "reasons": item.get("reasons") or [],
        }
