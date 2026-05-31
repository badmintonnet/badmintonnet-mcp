from api.recommendation_api import RecommendationAPI
from auth.request_context import get_access_token

api = RecommendationAPI()


def register_recommendation_tools(mcp):
    @mcp.tool()
    def get_personalized_badminton_recommendations(top: int = 2):
        """
        Get compact personalized badminton recommendations for the current user.
        Use for questions asking for suitable clubs, events, or tournaments.
        Returns at most 2 items per group with title, url, score, and short reasons.
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
