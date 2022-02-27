from os import access
from turtle import title
from django.test import TestCase, Client
from diary.models import User, Post
from rest_framework_simplejwt.tokens import RefreshToken


# Create your tests here.
class JWTTest(TestCase):
  fixtures = ['diary/fixtures/test/test_api_posts.json']

  def test_1(self):
    '''トークン取得できること'''
    response = Client().post(
      '/api/token/',
      data={
        'username': 'yhei',
        'password': 'password',
      }
    )
    print(response.json())
    self.assertTrue('refresh' in response.json().keys())
    self.assertTrue('access' in response.json().keys())

  def test_2_1(self):
    '''トークンを用いて日記を登録できること'''
    refresh = RefreshToken.for_user(User.objects.get(pk=1))
    response = Client().post(
        '/api/posts/',
        data={
          'title': 'title_for_test_2',
          'body': 'body_for_test_2',
        },
        content_type='application/json',
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )
    self.assertEqual(201, response.status_code)
    self.assertTrue(
      Post.objects.filter(
        title='title_for_test_2',
        body='body_for_test_2'
      ).exists()
    )

  def test_2_2(self):
    '''トークンを用いて日記を登録できること(トークン取得含む)'''
    # まずログインしてトークン取得
    response = Client().post(
      '/api/token/',
      data={
        'username': 'yhei',
        'password': 'password',
      }
    )
    access_token = response.json().get('access')
    response = Client().post(
        '/api/posts/',
        data={
          'title': 'title_for_test_2',
          'body': 'body_for_test_2',
        },
        content_type='application/json',
        # 取得したトークンを設定
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )
    self.assertEqual(201, response.status_code)
    self.assertTrue(
      Post.objects.filter(
        title='title_for_test_2',
        body='body_for_test_2'
      ).exists()
    )

  def test_3(self):
    '''トークンを用いない場合日記登録できないこと'''
    response = Client().post(
        '/api/posts/',
        data={
          'title': 'title_for_test_3',
          'body': 'body_for_test_3',
        },
        content_type='application/json',
    )
    self.assertEqual(401, response.status_code)

  def test_4(self):
    '''日記一覧はトークンがなくても取得できること'''
    response = Client().get(
        '/api/posts/',
        content_type='application/json',
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
        }
      ],
      response.json()
    )
