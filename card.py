from PokerGameBase import ImageSprite


class Card(object):
    # 1 is Clubs, 2 is diamonds, 3 is hearts, and 4 is spades
    # Suits are stored as integers so it is easier to randomize
    def __init__(self, rank, suit):
        if rank == 'A':
            self._rank = 14
        elif rank == 'K':
            self._rank = 13

        elif rank == 'Q':
            self._rank = 12
        elif rank == 'J':
            self._rank = 11
        else:
            self._rank = int(rank)

        if suit == 'C':
            self._suit = 1
        elif suit == 'D':
            self._suit = 2
        elif suit == 'H':
            self._suit = 3
        elif suit == 'S':
            self._suit = 4
        else:
            self._suit = int(suit)

    def getRank(self):
        return self._rank

    def getSuit(self):
        return self._suit

    def __repr__(self):
        value_name = ""
        suit_name = ""

        if self._rank == 14:
            value_name = "Ace"
        elif self._rank == 13:
            value_name = "King"
        elif self._rank == 12:
            value_name = "Queen"
        elif self._rank == 11:
            value_name = "Jack"
        elif self._rank == 10:
            value_name = "Ten"
        elif self._rank == 9:
            value_name = "Nine"
        elif self._rank == 8:
            value_name = "Eight"
        elif self._rank == 7:
            value_name = "Seven"
        elif self._rank == 6:
            value_name = "Six"
        elif self._rank == 5:
            value_name = "Five"
        elif self._rank == 4:
            value_name = "Four"
        elif self._rank == 3:
            value_name = "Three"
        elif self._rank == 2:
            value_name = "Two"

        if self._suit == 1:
            suit_name = "Clubs"
        elif self._suit == 2:
            suit_name = "Diamonds"
        elif self._suit == 3:
            suit_name = "Hearts"
        elif self._suit == 4:
            suit_name = "Spades"

        return value_name + " of " + suit_name

class CardImage(ImageSprite):
    ## Creates the constructor for the card class
    # @param rank is the value of the face of the card A,1,2,3...J,Q,K
    # @param int, suit is the suit of the card 1 = Club, 2 = diamond, 3 = Heart, 4 = Spade
    # displays the back of the card until flipped
    def __init__(self, x, y, rank, suit):
        self._fileName = "Images/back.bmp"
        self._xCoord = x
        self._yCoord = y
        super().__init__(self._xCoord, self._yCoord, self._fileName)

        if rank == 'A':
            self._rank = 14
        elif rank == 'K':
            self._rank = 13

        elif rank == 'Q':
            self._rank = 12
        elif rank == 'J':
            self._rank = 11
        else:
            self._rank = int(rank)

        if suit == 1:
            self._suit = 'C'
        elif suit == 2:
            self._suit = 'D'
        elif suit == 3:
            self._suit = 'H'
        elif suit == 4:
            self._suit = 'S'

    # Is an int
    def getImageRank(self):
        return self._rank

    # Is a string
    def getImageSuit(self):
        return self._suit

    ## Flips the Card Over and changes the image
    def flipCard(self):
        self._fileName = "Images/" + str(self._suit).lower() + str(self._rank) + ".bmp"
        super().__init__(self._xCoord, self._yCoord, self._fileName)