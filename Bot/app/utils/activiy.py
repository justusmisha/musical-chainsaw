from Bot.app.api.endpoints import UserEndpoints
from Bot.loader import api_client


async def activ_by_name(activ_name):
    result = await api_client.get(UserEndpoints.get_activity_by_name, name=activ_name)
    if not result or result is None:
        return False
    else:
        return result
