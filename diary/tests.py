from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import chromedriver_binary  # chromeのドライバーを自動インストール
from django.urls import reverse_lazy
from diary.models import Post, Star, User
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UiTest(StaticLiveServerTestCase):
  fixtures = ['diary/fixtures/test/test_index_view.json']

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.selenium = WebDriver()

  @classmethod
  def tearDownClass(cls):
    cls.selenium.quit()
    super().tearDownClass()

  def setUp(self) -> None:
    # ログイン
    self.selenium.get(self.live_server_url + '/admin/login/')
    username_input = self.selenium.find_element_by_name('username')
    username_input.send_keys('yhei')
    password_input = self.selenium.find_element_by_name('password')
    password_input.send_keys('password')
    self.selenium.find_element_by_css_selector('[type=submit]').click()

  def test_1(self):
    '''
    いいねするボタンを押したら、ボタンの名称が「いいね済」に変わること、いいねがDBに保存されること
    '''
    self.selenium.get('%s%s' % (self.live_server_url, str(reverse_lazy('diary:index'))))
    star_button_element = self.selenium.find_element_by_class_name('star--post-id-1')
    star_button_element.click()
    WebDriverWait(self.selenium, 2).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '.star--post-id-1.star--enabled'))
    )
    self.assertEqual('いいね済', star_button_element.text)
    self.assertEqual(
      True,
      Star.objects.filter(post__id=1, user__id=1).exists()
    )

  def test_2(self):
    '''
    いいね済ボタンを押したら、ボタンの名称が「いいねする」に変わること、いいねがDBから削除されていること
    '''
    # 予めいいねをしておく
    Star.objects.create(user=User.objects.get(id=1), post=Post.objects.get(id=1))

    self.selenium.get('%s%s' % (self.live_server_url, str(reverse_lazy('diary:index'))))
    star_button_element = self.selenium.find_element_by_class_name('star--post-id-1')
    star_button_element.click()
    WebDriverWait(self.selenium, 2).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '.star--post-id-1.star--enabled'))
    )
    self.assertEqual('いいねする', star_button_element.text)
    self.assertEqual(
      False,
      Star.objects.filter(post__id=1, user__id=1).exists()
    )
