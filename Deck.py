import random


class Deck:
    __nLands: int
    __nGoodLands: int
    __nCards: int

    def __init__(self, lands: int, good_lands: int, cards: int = 60):
        """
        :param lands: sets numbers of lands in deck
        :param good_lands: sets number of good lands in deck
        :param cards: sets total number of cards in deck
        """
        self.__nCards = cards
        self.__nGoodLands = good_lands
        self.__nLands = lands

    def draw(self):
        """
        Draws a random card from the deck
        :return: 0 = non_land, 1 = good_land, 2=non_good_land
        """
        # CardType = Tierra, Tierra buena, No_Tierra
        land_ratio = self.__nLands / self.__nCards
        good_lands_ratio = self.__nGoodLands / self.__nLands
        ret = 0
        if random.random() < land_ratio:
            # If True = Drew a land, if false, drew a non-land
            if random.random() < good_lands_ratio:
                # If True = Drew a good land, if false, drew a bad land
                # Good lands allows us to cast the desired spell (aka: matches the colors), bad lands don't
                self.__nGoodLands -= 1
                ret = 1
            else:
                # Non-good land
                ret = 2
            self.__nLands -= 1
        self.__nCards -= 1
        return ret
