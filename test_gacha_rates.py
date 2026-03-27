import simulation
import unittest
import gacha
from unittest.mock import patch
from simulation import GachaItem, Gacha, GenshinGachaSystem

MOCK_CHARACTER_RATES = {
    "five_star_rate": 6,
    "four_star_rate": 51,
    "pity_limit": 90,
    "soft_pity": 74,
    "four_star_pity": 10,
    "soft_pity_increase": 6
}

MOCK_WEAPON_RATES = {
        "name" : "Weapon Banner",
        "five_star_rate": 6,
        "four_star_rate": 51,
        "pity_limit": 80,
        "soft_pity": 64,
        "fifty-fifty" : True,
        "Chronicled" : False,
        "four_star_pity": 10,
        "soft_pity_increase": 6
    }

MOCK_BANNERS = {
    "Genshin": {
        "standard": MOCK_CHARACTER_RATES,
        "limited": MOCK_CHARACTER_RATES,
        "weapon": MOCK_WEAPON_RATES
    }
}

class TestGachaItem(unittest.TestCase):
    def test_getting_five_star(self):
        item = GachaItem(5)
        self.assertEqual(item.return_rarity(), 5)

    def test_getting_four_star(self):
        item = GachaItem(4)
        self.assertEqual(item.return_rarity(), 4)

    def test_getting_three_star(self):
        item = GachaItem(3)
        self.assertEqual(item.return_rarity(), 3)

class TestGacha(unittest.TestCase):
    def setUp(self):
        self._gacha = Gacha()
        self._gacha.get_pity(MOCK_CHARACTER_RATES)

    def test_pity_counter(self):
        self.assertEqual(self._gacha._five_star_pity, 90)
        self.assertEqual(self._gacha._four_star_pity, 10)
        self.assertEqual(self._gacha._soft_pity, 74)

    def test_starting_empty_list(self):
        self.assertEqual(self._gacha.get_rolls(), [])

    def test_rolling_appends_to_list(self):
        self._gacha.roll_gacha(MOCK_CHARACTER_RATES)
        self.assertEqual(len(self._gacha.get_rolls()), 1)

    def test_four_star_pity(self):
        self._gacha._four_star_pity = 0
        self._gacha.roll_gacha(MOCK_CHARACTER_RATES)
        item = self._gacha.get_rolls()[0]
        self.assertEqual(item.return_rarity(), 4)

    def test_five_star_pity(self):
        self._gacha._five_star_pity = 0
        self._gacha.roll_gacha(MOCK_CHARACTER_RATES)
        item = self._gacha.get_rolls()[0]
        self.assertEqual(item.return_rarity(), 5)

    def test_five_star_resets_soft_pity(self):
        with patch('simulation.randint', return_value = 1):
            self._gacha.roll_gacha(MOCK_CHARACTER_RATES)
            self.assertEqual(self._gacha._soft_pity, MOCK_CHARACTER_RATES["soft_pity"])

    def test_pity_decrements(self):
        initial_five = self._gacha._five_star_pity
        initial_four = self._gacha._four_star_pity
        with patch('simulation.randint', return_value = 500):
            self._gacha.roll_gacha(MOCK_CHARACTER_RATES)
        self.assertEqual(self._gacha._five_star_pity, initial_five - 1)
        self.assertEqual(self._gacha._four_star_pity, initial_four - 1)

    def test_get_rolls_returns_copy(self):
        self._gacha.roll_gacha(MOCK_CHARACTER_RATES)
        rolls = self._gacha.get_rolls()
        rolls.clear()
        self.assertEqual(len(self._gacha.get_rolls()), 1)



class TestGettingHoyoverseRates(unittest.TestCase):
    def test_getting_hoyoverse_gacha(self):
        self.assertEqual(type(gacha.get_banners('Genshin')), dict)

    def test_getting_information_from_gacha(self):
        info: dict = gacha.get_banners('Genshin')
        self.assertEqual(len(info), 3)
        limited = info['limited']
        self.assertEqual(limited['fifty-fifty'], True)
        self.assertEqual(limited['soft_pity_increase'], 6)

    def test_getting_information_from_weapon(self):
        info: dict = gacha.get_banners('Genshin')
        weapon = info['weapon']
        self.assertEqual(weapon['fifty-fifty'], True)
        self.assertEqual(weapon['Chronicled'], False)
        self.assertEqual(weapon['pity_limit'], 80)
        self.assertEqual(weapon['soft_pity'], 64)

    def test_getting_information_from_standard(self):
        info: dict = gacha.get_banners('Genshin')
        standard = info['standard']
        self.assertEqual(standard['fifty-fifty'], False)
        self.assertEqual(standard['pity_limit'], 90)

if __name__ == '__main__':
    unittest.main()
