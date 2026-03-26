banners = {
    "Genshin":{
    "standard" : {
        "name" : "Standard Banner",
        "five_star_rate": 6,
        "four_star_rate": 51,
        "pity_limit": 90,
        "soft_pity": 74,
        "fifty-fifty" : False,
        "four_star_pity" : 10,
        "soft_pity_increase" : 6
    },
    "limited" : {
        "name" : "Limited Banner",
        "five_star_rate": 6,
        "four_star_rate": 51,
        "pity_limit": 90,
        "soft_pity": 74,
        "fifty-fifty": True,
        "four_star_pity": 10,
        "soft_pity_increase": 6

    },
    "weapon" : {
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
}
}

def get_banners(gacha: str) -> dict:
    '''
    returns a gacha's banner's rates
    '''
    return banners[gacha]