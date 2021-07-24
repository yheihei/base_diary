from django.test import TestCase, Client
from rest_framework.test import APIClient
from diary.models import User
from rest_framework.authtoken.models import Token

# Create your tests here.
class TestApiPosts(TestCase):
  fixtures = ['diary/fixtures/test/test_api_posts.json']

  '''投稿のAPIテスト'''
  def test_1(self):
    '''投稿一覧が取得できるか'''
    token = Token.objects.get(user=User.objects.first())
    client = Client()
    response = client.get(
      '/api/posts/',
      HTTP_AUTHORIZATION=f"Token {token.pk}"
    )
    self.assertEqual(200, response.status_code)
    self.assertEqual(
      [
        {
          "id": 1,
          "user": {
            "id": 1,
            "username": "yhei",
            "email": "yheihei0126@gmail.com"
          },
          "title": "1つめの日記",
          "body": "1つめの日記本文",
          "created_at": "2021-07-13T05:10:40.097000Z",
          "updated_at": "2021-07-22T14:22:57.007000Z",
          "categories": [
            {
              "name": "日記",
              "slug": "diary"
            }
          ]
        },
        {
          "id": 2,
          "user": {
            "id": 1,
            "username": "yhei",
            "email": "yheihei0126@gmail.com"
          },
          "title": "2つめの日記",
          "body": "2つめの日記本文",
          "created_at": "2021-07-04T05:11:13.196000Z",
          "updated_at": "2021-07-22T13:59:50.294000Z",
          "categories": [
            {
              "name": "雑記",
              "slug": "general"
            }
          ]
        },
      ],
      response.json()
    )