from api.recommendation_api import RecommendationAPI
from auth.request_context import get_access_token

api = RecommendationAPI()


def register_recommendation_tools(mcp):
    @mcp.tool()
    def get_personalized_badminton_recommendations(top: int = 3):
        """
        Lay goi y ca nhan hoa cho nguoi dung dang dang nhap tren BadmintonNet.

        Use this tool when the user asks for personalized recommendations such as:
        - goi y CLB phu hop voi toi
        - co hoat dong nao gan toi / hop lich cua toi khong
        - toi nen tham gia giai dau nao
        - recommend clubs, activities, events, or tournaments for me

        The tool uses real system data: user location, skill rating, schedule,
        joined clubs, event history, tournament history, and available clubs/events/tournaments.

        Parameters
        ----------
        top : int
            Number of recommendations per group. Keep this small, usually 3.

        Returns
        -------
        JSON with profile, clubs, events, tournaments. Every item includes score,
        reasons, location, optional distanceKm/time/level, and url.
        """

        access_token = get_access_token()
        if not access_token:
            return {
                "error": "Nguoi dung chua dang nhap hoac thieu access token nen khong the goi y ca nhan hoa."
            }

        return api.get_personalized_recommendations(
            access_token=access_token,
            top=top,
        )
