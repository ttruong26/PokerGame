from PokerGameBase import GameBase
import pygame
from card import CardImage
from deck import Deck


GAME_WIDTH = 800
GAME_HEIGHT = 600


class Hand(list):
    def __init__(self):
        super().__init__()


class PokerGame(GameBase):
    deck = Deck()
    dealerHand = list()  # To display the card image of the dealer
    blinds = 20

    # Used to check the Cards of the river and
    checkPlayerHand = list()
    checkDealerHand = list()
    fiveCardPlayer = list()
    fiveCardDealer = list()

    def __init__(self):
        super().__init__(GAME_WIDTH, GAME_HEIGHT)
        self._cards = pygame.sprite.Group()
        self._bank = 500
        self._pot = 0
        self._round = 0

    def reset(self):
        self._sprites.empty()
        self._bank = self._bank - self.blinds
        self._pot += 2 * self.blinds
        self._round = 0
        self.playRiver()
        self.playHands()
        self.deck = Deck()  # Adds all the cards back to the deck

    def shuffleDeck(self):
        self.deck.shuffle()

    def playRiver(self):
        '''
        Prints the first three cards in the river
        :return:
        '''
        xStart = 120
        count = 0
        burnedCard = self.deck.deal()  # Burns a card before playing the river

        while count < 3:
            newCard = self.deck.deal()  # Deals a card from the deck and makes a new card object
            card = CardImage(xStart, 320, newCard.getRank(), newCard.getSuit())
            card.flipCard()

            xStart += 120
            count += 1

            self.checkDealerHand.append(newCard)
            self.checkPlayerHand.append(newCard)
            self._cards.add(card)
            self.add(card)

    def playHands(self):
        xPlayer = 310
        xDealer = 310
        yPlayer = 500
        yDealer = 150
        count = 0
        # Will play the players card, then dealers, in a snake format until they each have two
        while count < 4:
            # Will play the players card first
            if count % 2 == 0:
                newCard = self.deck.deal()
                card = CardImage(xPlayer, yPlayer, newCard.getRank(), newCard.getSuit())
                card.flipCard()
                xPlayer += 100
                count += 1
                self.checkPlayerHand.append(newCard)
                self._cards.add(card)
                self.add(card)
            else:
                newCard = self.deck.deal()
                card = CardImage(xDealer, yDealer, newCard.getRank(), newCard.getSuit())

                # Add a tuple containing the cards rank and suit info to a list
                self.dealerHand.append((newCard.getRank(), newCard.getSuit()))
                print(str(newCard.getRank()) + " : " + str(newCard.getSuit()))

                xDealer += 100
                count += 1
                self.checkDealerHand.append(newCard)
                self._cards.add(card)
                self.add(card)

    def showDealerHand(self):
        card1 = CardImage(310, 150, self.dealerHand[0][0], self.dealerHand[0][1])
        card2 = CardImage(410, 150, self.dealerHand[1][0], self.dealerHand[1][1])
        card1.flipCard()
        card2.flipCard()
        self._cards.add(card1)
        self.add(card1)
        self._cards.add(card2)
        self.add(card2)

    def addToRiver(self):
        round1XCoord = 480
        round2XCoord = 600

        if self._round == 1:
            burnCard = self.deck.deal()  # Burn a card before dealing a card
            newCard = self.deck.deal()
            card = CardImage(round1XCoord, 320, newCard.getRank(), newCard.getSuit())
            card.flipCard()

            self.checkDealerHand.append(newCard)
            self.checkPlayerHand.append(newCard)
            self._cards.add(card)
            self.add(card)

        elif self._round == 2:
            burnCard = self.deck.deal()
            newCard = self.deck.deal()
            card = CardImage(round2XCoord, 320, newCard.getRank(), newCard.getSuit())
            card.flipCard()

            self.checkDealerHand.append(newCard)
            self.checkPlayerHand.append(newCard)
            self._cards.add(card)
            self.add(card)

    def raiseBy(self):
        self._round += 1
        cont = True
        amount = int(input("Enter the an amount to wager:"))
        while cont:
            if amount <= self._bank:
                self._pot += 2 * amount
                self._bank -= amount
                self.addToRiver()
                cont = False
            else:
                print("Can not make a bet that is more than what you have.")
                amount = int(input("Enter an amount to wager: "))

    def check(self):
        self._round += 1
        self.addToRiver()

    def fold(self):
        self._round = 3

    def allIn(self):
        self._pot += 2 * self._bank
        self._bank = 0

        self._round += 1
        self.addToRiver()
        self._round += 1
        self.addToRiver()

    def deposit(self):
        amount = int(input("How much do you want to deposit: "))
        self._bank = self._bank + amount

    def cardCount(self, hand, value):
        """
        Finds the occurrences of the given card within a set
        :param set: is the set of 7 cards of either the user's hand or the AI's hand
        :param value: is the rank of the card we are trying to find the count for
        :return: The amount of occurrences Value has in the the user's/AI's hand
        """
        ranks = [card.getRank() for card in hand]
        rank_dict = dict()

        for rank in ranks:
            if rank not in rank_dict:
                rank_dict[rank] = 1
            else:
                rank_dict[rank] += 1

        return rank_dict[value]

    def highCard(self, hand):
        """
        Finds the high card in a hand of cards
        :param set: is the set of 7 cards of either the user's hand or the AI's hand
        :return: returns the highest card within a set of cards
        """
        ranks = [card.getRank() for card in hand]

        return max(ranks)

    def isPair(self, hand):
        """
        Checks if there is at least one two pair in the set of cards
        :param list: is the list of 7 cards of either the user's hand or the AI's hand
        :return: True if at least one two pair is found, False if there are no pairs found
        """
        ranks = [card.getRank() for card in hand]
        pairList = list()
        for rank in ranks:
            if self.cardCount(hand, rank) >= 2:
                pairList.append(rank)
        if not pairList:
            return False, 0
        else:
            return True, max(pairList)  # Return True and the highest rank if there are multiple pairs

    def hasPair(self, hand, value):
        if self.cardCount(hand, value) >= 2:
            return True
        else:
            return False

    def isTwoPair(self, hand):
        """
        Checks if a pair occurrence appears more than twice
        :param list: is the list of 7 cards of either the user's hand or the AI's hand
        :return: True if two or more pairs are found in a hand, False if not
        """
        ranks = [card.getRank() for card in hand]
        pairCount = 0
        pairList = list()

        for rank in ranks:
            if self.hasPair(hand, rank) and rank not in pairList:
                pairCount += 1
                pairList.append(rank)
        print(pairList)
        if pairCount >= 2:
            return True, max(pairList)
        else:
            return False, 0

    def isThreeOf(self, hand):
        """
        Checks if there is at least three of a kind in a hand
        :param list: is the list of 7 cards of either the user's hand or the AI's hand
        :return: True if there are Three cards of the same rank found. False if not
        """
        ranks = [card.getRank() for card in hand]
        threeOfList = list()
        # Iterates through all the ranks in a hand and checks if there is Three of a kind for each rank
        for rank in ranks:
            if self.cardCount(hand, rank) >= 3:
                threeOfList.append(rank)
        if not threeOfList:
            return False, 0
        else:
            return True, max(threeOfList)

    def isFourOf(self, hand):
        """
        Checks if there is Four of a kind in a hand
        :param list: is the list of 7 cards of either the user's hand or the AI's hand
        :return: True if Four cards of the same rank are found. False if not
        """
        ranks = [card.getRank() for card in hand]
        for rank in ranks:
            if self.cardCount(hand, rank) == 4:
                return True, rank  # Return the value of the 4 of a kind and True

        return False, 0  # Four of a kind not found

    def isFullHouse(self, hand):
        """
        Finds if there is a full house in a hand. Full house is a hand of with a three pair and a two pair
        :param list: is the list of 7 cards of either the user's hand or the AI's hand
        :return: True if the there is a two pair and a three pair found in the hand of seven
        """
        threeOF = 0
        if self.isThreeOf(hand)[0]:
            threeOF = self.isThreeOf(hand)[1]
        if self.isPair(hand)[0] and self.isThreeOf(hand)[0]:
            return True, threeOF  # Return True and the value of the three of a kind
        else:
            return False, 0

    def isStraight(self, hand):
        """
        Will check if there are 5 consecutive cards in order by rank. Ace can be used to either start a straight followed
        up by two or end a straight after a king, but can not be used in middle. Disregards the face of the cards

        :param hand: is the list of 7 cards of either the user's hand or the AI's hand
        :return: True if 5 cards are in consecutive order, False otherwise.
        """
        ranks = list()
        for card in hand:
            ranks.append(card.getRank())
        count = 0


        # Iterates from 14,2,3,4,... to 14 because ace holds the value 14
        for rank in (14, *range(2, 15)):
            if rank in ranks:
                count += 1
                if count >= 6:
                    return True, rank   # Return True and the highest value in the straight
                elif count == 5:
                    return True, rank
                else:
                    count = 0
            else:
                return False, 0

    def isFlush(self, hand):
        """
        Checks if there are 5 of the same suit cards in a hand
        :param list: is the list of 7 cards of either the user's hand or the AI's hand
        :return: True if there is 5 occurrences of a single suit, False if not
        """
        cards = hand
        flushCards = list()
        suits_dic = dict()
        flush = False

        # Gathers the count for each face and stores it into a dictionary
        for card in cards:
            if card.getSuit() in suits_dic:
                suits_dic[card] += 1
            else:
                suits_dic[card] = 1

        suit_values = suits_dic.values()   # Stores the count of each face into a list
        if max(suit_values) >= 5:
            flush = True

        # If there is a flush, then we add all cards that match the suit of the flush into a list
        for card in cards:
            if flush and card.getSuit() == max(suits_dic, key=suits_dic.get):
                flushCards.append(card)


        # flushCards will be empty if flush never gets set to true
        if not flushCards:
            return flush, 0  # That means flush will be false
        else:
            flushRanks = [card.getRank() for card in flushCards]  # Stores the rank of the cards that are apart of the flush
            return flush, max(flushRanks)  # True and the highest Card within the flush

    def isStraightFlush(self, hand):
        """
        Checks if there is a straight Flush in a hand
        :param list: is the list of 7 cards of either the user's hand or the AI's hand
        :return: True if there is a flush and a straight found, False if both are not found
        """
        if self.isStraight(hand)[0] and self.isFlush(hand)[0]:
            return True, self.isStraight(hand)[1]
        else:
            return False, 0

    def isRoyalFlush(self, hand):
        """
        Checks if there is a Royal Flush in a hand of poker
        :param list: is the list of 7 cards of either the user's hand or the AI's hand
        :return: True if a straight Flush is found, and the hand contains the cards 10-Ace, False if not
        """
        ranks = [card.getRank() for card in hand]
        # Checks if the hand is a straight flush, and if it contains cards 10 - Ace
        if self.isStraightFlush(hand) and all(rank in ranks for rank in [10, 11, 12, 13, 14]):
            return True, 14
        else:
            return False, 0

    def checkHand(self, hand):
        if self.isRoyalFlush(hand)[0]:
            return 9, self.isRoyalFlush(hand)[1]
        elif self.isStraightFlush(hand)[0]:
            return 8, self.isStraightFlush(hand)[1]
        elif self.isFourOf(hand):
            return 7, self.isFourOf(hand)[1]
        elif self.isFullHouse(hand):
            return 6, self.isFullHouse(hand)[1]
        elif self.isFlush(hand):
            return 5, self.isFlush(hand)[1]
        elif self.isStraight(hand):
            return 4, self.isStraight(hand)[1]
        elif self.isThreeOf(hand):
            return 3, self.isThreeOf(hand)[1]
        elif self.isTwoPair(hand):
            return 2, self.isTwoPair(hand)[1]
        elif self.isPair(hand):
            return 1, self.isPair(hand)[1]
        else:
            return 0, self.highCard(hand)

    def determineWinner(self):
        if self.checkHand(self.checkPlayerHand)[0] > self.checkHand(self.checkDealerHand)[0]:
            print("The user wins this round")
            self._bank += self._pot
            self._pot = 0
        elif self.checkHand(self.checkDealerHand)[0] > self.checkHand(self.checkPlayerHand)[0]:
            print("You lose, the ai gets all of the pot")
            self._pot = 0
        else:
            if self.checkHand(self.checkPlayerHand)[1] > self.checkHand(self.checkDealerHand)[1]:
                print("The user wins this round")
                self._bank += self._pot
                self._pot = 0
            elif self.checkHand(self.checkDealerHand)[1] > self.checkHand(self.checkPlayerHand)[1]:
                print("You lose, the ai gets all of the pot")
                self._pot = 0
            else:
                print("You tie, you get half of the money back")
                self._bank += self._pot / 2
                self._pot = 0

    def showPotandBank(self):
        self.displayText("Pot: $" + str(self._pot), 0, 0, "left")
        self.displayText(("Bank: $" + str(self._bank)), self._width, self._height, "right")

    def showBank(self):
        self.displayText(("Bank: $" + str(self._bank)), self._width, self._height, "right")
        self.displayButton('Deposit', self._width - 100, self._height - 40, 100, 40, self.deposit)

    def showButton(self):
        self.displayButton('Fold', 0, self._height, 100, 40, self.fold)
        self.displayButton('Check', 0, self._height - 50, 100, 40, self.check)
        self.displayButton('Raise', 0, self._height - 100, 100, 40, self.raiseBy)
        self.displayButton('All In', 0, self._height - 150, 100, 40, self.allIn)
        self.displayButton('Deposit', self._width - 100, self._height - 40, 100, 40, self.deposit)
        self.displayButton('Reset', self._width - 100, self._height - 90, 100, 40, self.reset)

    def update(self):
        super().update()
        if self.getTicks() == 10:
            self._bank = self._bank - self.blinds
            self._pot += 2 * self.blinds
            self.shuffleDeck()
            self.playHands()
            self.playRiver()

        if self._round >= 2:
            self.showDealerHand()
            print("Two pair: " + str(self.isTwoPair(self.checkPlayerHand)))
            print("Three of: " + str(self.isThreeOf(self.checkPlayerHand)))
            print("Is pair: " + str(self.isPair(self.checkPlayerHand)))
            print("Is straight: "+ str(self.isStraight(self.checkPlayerHand)))
            print("Is Full house: "+ str(self.isFullHouse(self.checkPlayerHand)))
            print("Is straight Flush: " + str(self.isStraightFlush(self.checkPlayerHand)))
            print("Is Flush: " + str(self.isFlush(self.checkPlayerHand)))
            print("Is royal flush" + str(self.isRoyalFlush(self.checkPlayerHand)))
            print("Two pair: " + str(self.isTwoPair(self.checkDealerHand)))
            print("Three of: " + str(self.isThreeOf(self.checkDealerHand)))
            print("Is pair: " + str(self.isPair(self.checkDealerHand)))
            print("Is straight: "+ str(self.isStraight(self.checkDealerHand)))
            print("Is Full house: " + str(self.isFullHouse(self.checkDealerHand)))
            print("Is straight Flush: " + str(self.isStraightFlush(self.checkDealerHand)))
            print("Is Flush: " + str(self.isFlush(self.checkDealerHand)))
            print("Is royal flush" + str(self.isRoyalFlush(self.checkDealerHand)))

            self.determineWinner()

def main():
    cardGame = PokerGame()
    cardGame.run()


if __name__ == "__main__":
    main()
