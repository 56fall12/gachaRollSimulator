import unittest
import gacha

class TestGettingHoyoverseRates(unittest.TestCase):
    def test_getting_hoyoverse_gacha(self):
        self.assertEqual(type(gacha.get_banners('Hoyoverse')), dict)

    def test_getting_information_from_gacha(self):
        info: dict = gacha.get_banners('Hoyoverse')
        self.assertEqual(len(info), 3)
        limited = info['limited']
        self.assertEqual(limited['fifty-fifty'], True)

if __name__ == '__main__':
    unittest.main()