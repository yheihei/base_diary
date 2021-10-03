import requests
from django.core.exceptions import PermissionDenied


class TweetGetTimelineService:
  def __init__(self, user_id) -> None:
    self.__user_id = user_id
  
  def get(self):
    params = {
      # 何かリクエストに必要なやつがここに入るが今は関係ない
    }
    response = requests.get(
      f'https://api.twitter.com/2/users/{str(self.__user_id)}/tweets',
      params=params
    )
    if response.status_code == 401:
      raise PermissionDenied(response.json())
    return response.json().get('data', [])
