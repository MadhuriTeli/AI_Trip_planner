
from langchain_tavily import TavilySearch


class TavilyPlaceSearchTool:
    """
    Free/low-cost place search using Tavily.
    Replaces GooglePlacesTool so no GPLACES_API_KEY is required.
    """

    def __init__(self):
        self.tavily_tool = TavilySearch(
            topic="general",
            include_answer="advanced"
        )

    def _search(self, query: str):
        result = self.tavily_tool.invoke({"query": query})

        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]

        return result

    def tavily_search_attractions(self, place: str):
        return self._search(
            f"top tourist attractions and places to visit in and around {place}"
        )

    def tavily_search_restaurants(self, place: str):
        return self._search(
            f"top 10 restaurants, cafes and eateries in and around {place}"
        )

    def tavily_search_activity(self, place: str):
        return self._search(
            f"popular activities and things to do in and around {place}"
        )

    def tavily_search_transportation(self, place: str):
        return self._search(
            f"best transportation options, public transport, taxis and local travel "
            f"options available in {place}"
        )


# Backward-compatible alias.
# This allows existing code that imports GooglePlaceSearchTool
# to continue working without Google Places.
class GooglePlaceSearchTool:
    """
    Compatibility wrapper.
    Uses Tavily instead of Google Places.
    """

    def __init__(self, api_key=None):
        self.tavily_tool = TavilyPlaceSearchTool()

    def google_search_attractions(self, place: str):
        return self.tavily_tool.tavily_search_attractions(place)

    def google_search_restaurants(self, place: str):
        return self.tavily_tool.tavily_search_restaurants(place)

    def google_search_activity(self, place: str):
        return self.tavily_tool.tavily_search_activity(place)

    def google_search_transportation(self, place: str):
        return self.tavily_tool.tavily_search_transportation(place)
