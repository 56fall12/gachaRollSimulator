
from gacha import banners
from random import randint

class GachaItem:
    def __init__(self,  rarity):
        self._rarity = rarity

    def return_rarity(self) -> int:
        '''
        return the rarity of the item
        Returns:
            int
        '''
        return self._rarity

class Gacha:
    def __init__(self):
        self._rolls: list = []
        self._current_roll_count: int = 0
        self._four_star_pity: int | None = None
        self._five_star_pity: int | None = None
        self._soft_pity: int | None = None

    def get_pity(self, gacha_rates: dict) -> None:
        '''
        set the pity for the gacha if there is any
        Args:
            gacha_rates(dict): dict with keys "five_star_pity" and "four_star_pity" and
                                                "soft_pity"
        Returns:
            None
        '''
        if "pity_limit" in gacha_rates:
            self._five_star_pity = gacha_rates["pity_limit"]

        if "four_star_pity" in gacha_rates:
            self._four_star_pity = gacha_rates["four_star_pity"]
        if "soft_pity" in gacha_rates:
            self._soft_pity = gacha_rates["soft_pity"]

    def get_rolls(self) -> list:
        '''
        return the list of rolls gotten
        '''
        return self._rolls.copy()

    def roll_gacha(self, gacha_rates: dict):
        '''
        Rolls the gacha based on provided rates.
        Args:
            gacha_rates(dict): dict with keys "five_star_rate" and "four_star_rate",
                            representing cumulative thresholds out of 1000.
                            e.g. {"five_star_rate": 10, "four_star_rate": 110}
        Returns:
            None
        '''
        if self._four_star_pity == 0:
            item = GachaItem(4)
        elif self._five_star_pity == 0:
            item = GachaItem(5)
        else:
            result = randint(1,1000)
            if self._soft_pity is not None:
                self._soft_pity -= 1
            if self._four_star_pity is not None:
                self._four_star_pity -= 1
            if self._five_star_pity is not None:
                self._five_star_pity -= 1
            if result <= (gacha_rates["five_star_rate"] + (gacha_rates["soft_pity_increase"] * (self._soft_pity * -1))  if self._soft_pity is not None and self._soft_pity < 0
                                                            else gacha_rates["five_star_rate"]):
                item = GachaItem(5)
                self._five_star_pity = gacha_rates["pity_limit"]
                self._soft_pity = gacha_rates["soft_pity"]

            elif gacha_rates["five_star_rate"] < result <= gacha_rates["four_star_rate"]:
                item = GachaItem(4)
                self._four_star_pity = gacha_rates["four_star_pity"]
            else:
                item = GachaItem(3)

        self._rolls.append(item)


class GenshinGachaSystem(Gacha):
    def __init__(self, banner_type: str):
        super().__init__()
        self._banner_type = self.validate_banner_type(banner_type)
        self.get_pity(self._banner_type)


    def validate_banner_type(self, banner_type: str) -> dict:
        '''
        Checks whether the banner type is valid
        Args:
            banner_type: checks if the banner type is valid e.g.("standard", "character")

        Returns:
            dict
        '''
        if banner_type not in banners["Genshin"]:
            raise ValueError(f"Invalid banner type: {banner_type}")
        return banners["Genshin"][banner_type]

    def roll(self, amount: int) -> list:
        return [super().roll_gacha(self._banner_type) for i in range(amount)]



