from Deck import Deck


class Simul:
    __starting_Hand_Size: int = 7
    __n_Iterations: int = 1000000  # A million simulations per set

    def __init__(self, starting_hand_size: int = 7, n_iterations: int = 1000000):
        """
            Starts simul with the given params
            :param n_lands: number of lands in deck
            :param cmc: mana value of the card to cast. Expected to be cast on curve, so cmc = turn to be casted!
            :param n_cards: number of starting cards in the deck
            :param colors_needed: number of colored sources needed to cast the spell.
            :return: Something
            i.e: "Wrath of god has a CMC=4, colors_needed=2, since it costs {2ww}
        """
        # The entire simulation is based on being on the play since the odds of drawing the required sources on the
        # draw are higher (because we take an extra draw step), so we take "on the play" odds, which are "worse" for
        # mana base restrictions.
        self.__starting_Hand_Size = starting_hand_size
        self.__n_Iterations = n_iterations

    def start_simul(self, n_lands: int, cmc: int, n_cards: int, colors_needed: int):
        """
        Finds the minimum number of good lands needed in a n_lands deck with n_cards to cast our most restrictive card
        on curve. The cut off is 90+{CMC}% or 95% of the time we hit the required land drops.
        If no combination is found, returns the minimum number of good lands needed equal to n_lands.
        :param n_lands: total number of lands/mana sources in the starting deck
        :param cmc: Converted mana cost we want to curve into
        :param n_cards: Number of cards in the starting deck
        :param colors_needed: Number of needed colored sources needed to cast the most restrictive spell on our deck.
        :return: n_good_lands with expected mulligan rate and curving landrops to CMC.
        """
        for n_good_lands in reversed(range(colors_needed, n_lands)):
            # We need at least "colors_needed" good sources to cast the given spell.
            count_lands_ok = 0  # Number of games with enough lands drawn
            count_lands_great = 0  # Number of games with enough lands drawn AND the right colored sources
            n_mulligans = 0  # Number of mulligans taken in total
            for i in range(0, self.__n_Iterations):
                lands_in_hand = 0
                good_lands_in_hand = 0
                deck = Deck(lands=n_lands, good_lands=n_good_lands, cards=n_cards)
                # Draw starting hand of starting_hand_size
                for x in range(0, self.__starting_Hand_Size):
                    lands_in_hand, good_lands_in_hand = self.new_card(lands_in_hand, good_lands_in_hand, deck)

                # We mulligan hands with less than 2 lands and with more than 4 lands, for simplicity reasons.
                if lands_in_hand < 2 or lands_in_hand > 4:
                    # Accounting current mulligan rules, the starting hands are always 7 + bottoming a card,
                    # so we are not repeating the simul as if this was the London nor Vancouver mulligan rule,
                    # but we count how many mulls we have taken.
                    n_mulligans += 1
                    continue

                # We continue to draw cards until CMC of the card is reached
                for x in range(1, cmc):
                    lands_in_hand, good_lands_in_hand = self.new_card(lands_in_hand, good_lands_in_hand, deck)

                # We count if the hand had enough lands and if the lands were good enough to cast our restrictive spells
                if lands_in_hand >= cmc and good_lands_in_hand >= colors_needed:
                    # We had enough lands, and them were good!
                    count_lands_great += 1
                    count_lands_ok += 1
                elif lands_in_hand >= cmc:
                    # We had enough lands but they were not good enough
                    count_lands_ok += 1
            # End of the 1000000 iterations
            success_rate = (count_lands_great / count_lands_ok) * 100.0
            curving_landrops = (count_lands_ok / (self.__n_Iterations - n_mulligans)) * 100.0
            mulligan_rate = (n_mulligans / self.__n_Iterations) * 100.0
            # print("Number of good lands: %d, success rate = %f " % (n_good_lands, success_rate))
            # print("The deck hits enough landrops with a success rate of %f" % curving_landrops)
            # print("The deck had a mulligan rate of %f in total" % mulligan_rate)
            # print("--------------------------------------------------------------------------------")
            if success_rate <= min((90 + cmc), 95):
                return success_rate, curving_landrops, mulligan_rate, n_good_lands

    @staticmethod
    def new_card(lands_in_hand, good_lands_in_hand, deck):
        card = deck.draw()
        if card == 1:
            lands_in_hand += 1
            good_lands_in_hand += 1
        elif card == 2:
            lands_in_hand += 1
        return lands_in_hand, good_lands_in_hand
