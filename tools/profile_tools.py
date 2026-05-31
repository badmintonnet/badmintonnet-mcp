from api.profile_api import ProfileAPI
from auth.request_context import get_access_token

api = ProfileAPI()


def _club_refs(clubs, limit: int = 3):
    if not isinstance(clubs, list):
        return []

    result = []
    for club in clubs[:limit]:
        if not isinstance(club, dict):
            continue
        result.append({
            "clubName": club.get("clubName") or club.get("name"),
            "slug": club.get("slug"),
        })
    return result


def _slim_account(account: dict):
    if not isinstance(account, dict):
        return account

    return {
        "fullName": account.get("fullName"),
        "email": account.get("email"),
        "phone": account.get("phone"),
        "gender": account.get("gender"),
        "address": str(account.get("address") or "")[:160],
        "reputationScore": account.get("reputationScore"),
        "totalParticipatedEvents": account.get("totalParticipatedEvents"),
        "ownerClubs": _club_refs(account.get("ownerClubs")),
        "myClubs": _club_refs(account.get("myClubs")),
    }


def register_profile_tools(mcp):
    @mcp.tool()
    def get_my_profile_data():
        """
        Get a compact account summary for the current authenticated user.
        Use for "who am I" or questions about the user's own profile/clubs.
        """

        access_token = get_access_token()

        response_json = api.get_account(access_token=access_token)

        if isinstance(response_json, dict):
            return _slim_account(response_json.get("data") or {})

        return response_json

    @mcp.tool()
    def get_my_player_rating():
        """
        Get the current user's badminton skill rating summary.
        """

        access_token = get_access_token()

        return api.get_player_rating(access_token=access_token)

    @mcp.tool()
    def get_my_schedule():
        """
        Get up to 5 current schedule items for the authenticated user.
        """

        access_token = get_access_token()

        return api.get_schedule(
            access_token=access_token,
            page=0,
            size=5,
        )

def find_user_nearby_tools(mcp):    
    @mcp.tool()
    def get_nearby_badminton_players(
    ):
        """
        Lấy danh sách các người chơi cầu lông ở gần vị trí của người dùng.

        Get a list of nearby badminton players based on the user's location.


        Returns
        -------
        Trả về dữ liệu phân trang chứa danh sách người chơi gần người dùng, có địa chỉ địa chỉ cụ thể

        A paginated JSON response containing a list of badminton players nearby user, and have specific address.
        """

        access_token = get_access_token()

        return api.get_nearby_badminton_players(
            access_token=access_token,  
        )
