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
            params={"top": max(1, min(top, 2))},
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
        }

    def _slim_profile(self, profile: dict):
        return {
            "fullName": profile.get("fullName"),
            "skillScore": profile.get("skillScore"),
            "skillLevel": profile.get("skillLevel"),
            "hasLocation": profile.get("hasLocation"),
        }

    def _slim_items(self, items: list[dict]):
        return [self._slim_item(item) for item in items[:2]]

    def _slim_item(self, item: dict):
        return {
            "type": item.get("type"),
            "title": item.get("title"),
            "url": item.get("detailUrl"),
            "clubName": item.get("clubName"),
            "location": item.get("location"),
            "score": item.get("score"),
            "distanceKm": item.get("distanceKm"),
            "fee": item.get("fee"),
            "startTime": item.get("startTime"),
            "reasons": self._short_list(item.get("reasons") or [], limit=2),
        }

    def _short_list(self, values: list, limit: int = 2):
        out = []
        for value in values[:limit]:
            text = str(value).strip()
            if text:
                out.append(text[:120])
        return out
