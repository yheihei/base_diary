from django.test import TestCase

# Create your tests here.
class CITest(TestCase):
  def test_1(self):
    print('絶対に通るテスト')
    self.assertEqual(True, True)
