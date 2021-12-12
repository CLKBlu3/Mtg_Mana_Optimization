from Deck import Deck
import argparse

from Simul import Simul


def main():
    """
    PRE:
      1. Good lands needed
      2. CMC (Turn allowed)
      3. Good lands needed <= CMC (Turn allowed)
      i.e: Wrath of god is {2ww}, so --> Good lands needed = 2 (ww colored sources), cmc=4 (Turn to be casted)
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("nLands", help="Total number of lands in the deck. (int), mandatory.", type=int)
    parser.add_argument("cmc", help="CMC of the card desired to cast. (int)", type=int)
    parser.add_argument("colors_needed", help="Number of colored sources to cast the spell. (int)", type=int, default=0)
    parser.add_argument("nCards", help="Total number of  cards in the deck. (int) Default: 60", type=int, default=60)
    args = parser.parse_args()
    n_lands = args.nLands
    if n_lands <= 3:
        print("The number of lands can't be smaller than 4!")
        return -1

    cmc = args.cmc
    if n_lands < cmc:
        print("Can't cast a spell without enough lands in the deck!")
        return -1

    n_cards = args.nCards
    if n_lands >= n_cards:
        print("The number of lands can't be equal or higher to the number of cards in the deck!")
        return -1
    colors_needed = args.colors_needed
    Simul(n_lands, cmc, n_cards, colors_needed)
    return 0


if __name__ == '__main__':
    main()
