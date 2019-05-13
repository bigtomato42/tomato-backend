from django.test import TestCase

class RandomTestCase(TestCase):
    def setUp(self):
        pass

    def test_stuff(self):
        print("works !")
        return True
