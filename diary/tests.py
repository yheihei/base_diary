from django.test import TestCase, Client
from unittest.mock import patch
from diary.services import TweetGetTimelineService
from django.core.exceptions import PermissionDenied
from django.urls import reverse


class TweetGetTimelineMockResponse:
  def __init__(self):
    self.status_code = 200

  def json(self):
    '''
    APIレファレンス TimeLines GET /2/users/:id/tweets
    https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
    '''
    return {
      "data": [
        {
          "id": "3",
          "text": "つぶやき3"
        },
        {
          "id": "2",
          "text": "つぶやき2"
        },
        {
          "id": "1",
          "text": "つぶやき1"
        },
      ],
      "meta": {
        "oldest_id": "1",
        "newest_id": "3",
        "result_count": 3,
        "next_token": "7140dibdnow9c7btw3w29grvxfcgvpb9n9coehpk7xz5i"
      }
    }

class TweetGetTimelineMockResponse401:
  def __init__(self):
    self.status_code = 401

  def json(self):
    return {
      'title': 'Unauthorized',
      'detail': 'Unauthorized',
      'type': 'about:blank',
      'status': 401
    }


# Create your tests here.
class TweetGetTimelineServiceTest(TestCase):
  @patch("requests.get", return_value=TweetGetTimelineMockResponse())
  def test_1(self, mocked):
    '''
    ユーザーのタイムラインを正常に取得できること
    '''
    service = TweetGetTimelineService(user_id=1)
    timelines = service.get()
    self.assertEqual(True, len(timelines) > 0)
    self.assertEqual(
      '3',
      timelines[0].get('id')
    )
    self.assertEqual(
      'つぶやき3',
      timelines[0].get('text')
    )

  @patch("requests.get", return_value=TweetGetTimelineMockResponse401())
  def test_2(self, mocked):
    '''
    ユーザーのタイムラインが401で取得できなかったときPermissionDeniedが発生すること
    '''
    service = TweetGetTimelineService(user_id=1)
    with self.assertRaises(PermissionDenied):
      service.get()


class IndexViewTest(TestCase):
  @patch("requests.get", return_value=TweetGetTimelineMockResponse())
  def test_1(self, mocked):
    '''
    ユーザのタイムラインがトップページに表示されていること
    '''
    response = Client().get(reverse('diary:index'))
    timelines = response.context['timelines']
    self.assertEqual(True, len(timelines) > 0)
    self.assertEqual(
      '3',
      timelines[0].get('id')
    )
    self.assertEqual(
      'つぶやき3',
      timelines[0].get('text')
    )

  @patch("requests.get", return_value=TweetGetTimelineMockResponse401())
  def test_2(self, mocked):
    '''
    ユーザのタイムラインが401で取得できなかった時 トップページに表示されていないこと
    '''
    response = Client().get(reverse('diary:index'))
    timelines = response.context['timelines']
    self.assertEqual(0, len(timelines))
