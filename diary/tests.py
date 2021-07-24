from django.test import TestCase, Client
from diary.models import User, Post
from rest_framework.authtoken.models import Token
from django.urls import reverse

# Create your tests here.
class TestApiPosts(TestCase):
  '''投稿のAPIテスト'''
  fixtures = ['diary/fixtures/test/test_api_posts.json']

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
          "created_at": "2021-07-03T05:10:40.097000Z",
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

  def test_2(self):
    '''カテゴリで検索できるか'''
    token = Token.objects.get(user=User.objects.first())
    client = Client()
    response = client.get(
      '/api/posts/',
      {
        'category': 'diary',
      },
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
          "created_at": "2021-07-03T05:10:40.097000Z",
          "updated_at": "2021-07-22T14:22:57.007000Z",
          "categories": [
            {
              "name": "日記",
              "slug": "diary"
            }
          ]
        },
      ],
      response.json()
    )

  def test_3(self):
    '''キーワード検索できるか'''
    token = Token.objects.get(user=User.objects.first())
    client = Client()
    response = client.get(
      '/api/posts/',
      {
        'search': '2つめ',
      },
      HTTP_AUTHORIZATION=f"Token {token.pk}"
    )
    self.assertEqual(200, response.status_code)
    self.assertEqual(
      [
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

  def test_5(self):
    '''投稿日時の降順で取得できるか'''
    token = Token.objects.get(user=User.objects.first())
    client = Client()
    response = client.get(
      '/api/posts/',
      {
        'ordering': '-created_at',
      },
      HTTP_AUTHORIZATION=f"Token {token.pk}"
    )
    self.assertEqual(200, response.status_code)
    self.assertEqual(
      [
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
        {
          "id": 1,
          "user": {
            "id": 1,
            "username": "yhei",
            "email": "yheihei0126@gmail.com"
          },
          "title": "1つめの日記",
          "body": "1つめの日記本文",
          "created_at": "2021-07-03T05:10:40.097000Z",
          "updated_at": "2021-07-22T14:22:57.007000Z",
          "categories": [
            {
              "name": "日記",
              "slug": "diary"
            }
          ]
        },
      ],
      response.json()
    )

  def test_6(self):
    '''新規投稿できるか'''
    token = Token.objects.get(user=User.objects.first())
    client = Client()
    response = client.post(
      '/api/posts/',
      {
        'title': 'title for test_6',
        'body': 'body for test_6',
      },
      content_type='application/json',
      HTTP_AUTHORIZATION=f"Token {token.pk}"
    )
    self.assertEqual(201, response.status_code)
    post = Post.objects.get(title='title for test_6')
    self.assertEqual('body for test_6', post.body)
    self.assertEqual(User.objects.first(), post.user)

  def test_7(self):
    '''PUTでの更新ができるか'''
    token = Token.objects.get(user=User.objects.first())
    client = Client()
    response = client.put(
      '/api/posts/1/',
      {
        'title': '1つめの日記 modified',
        'body': '1つめの日記本文 modified',
      },
      content_type='application/json',
      HTTP_AUTHORIZATION=f"Token {token.pk}"
    )
    self.assertEqual(200, response.status_code)
    post = Post.objects.get(id=1)
    self.assertEqual('1つめの日記 modified', post.title)
    self.assertEqual('1つめの日記本文 modified', post.body)