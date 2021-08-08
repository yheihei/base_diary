from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import chromedriver_binary  # chromeのドライバーを自動インストール
from django.urls import reverse_lazy


# Create your tests here.
class UiTest(LiveServerTestCase):
  fixtures = ['diary/fixtures/test/test_index_view.json']

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.selenium = WebDriver()

  @classmethod
  def tearDownClass(cls):
    cls.selenium.quit()
    super().tearDownClass()

  def test_1(self):
    self.selenium.get('%s%s' % (self.live_server_url, str(reverse_lazy('diary:index'))))
    print('%s%s' % (self.live_server_url, str(reverse_lazy('diary:index'))))
    headline = self.selenium.find_element(By.TAG_NAME, 'h1')
    self.assertEqual('とあるエンジニアの日記帳', headline.text)
