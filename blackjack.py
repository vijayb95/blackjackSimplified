import random, time

userCards = []

def main():
    print("**************************** Welcome to BlackJack ****************************")
    count = 0
    user = getUser()
    print(f"\nHi {(user.user).capitalize()}, your current balance in BlackJack wallet is ${user.balance}\n")
    while True:
        time.sleep(1.5)
        deck = Deck()
        deck.shuffle()
        betAmt = bet(user)
        print("\nLet the Game Begins!\n\nLoading... ")
        time.sleep(3)
        dealerCards = []
        userTotal = 0
        dealerTotal = 0
        while True:
            if count == 0:
                count += 1
                userCards.append(deck.drawCard(userTotal))
                userCards.append(deck.drawCard(userTotal))
                dealerCards.append(deck.drawCard(dealerTotal))
                dealerCards.append(deck.drawCard(dealerTotal))
                userTotal = total(userCards)
                print(f"\nThe Cards {user.user.capitalize()} have are: ")
                for card in userCards:
                    card.show()
                    time.sleep(0.5)
                print(f"\nThe total value of your card is {userTotal} points\n")
                time.sleep(1)
                print(f"The Cards Dealer have are: ")
                dealerCards[0].show()
                print("This card is hidden\n")
                dealerTotal = total(dealerCards)
            else:
                time.sleep(1)
                choice = input("You wanna hit or stand? (H for hit, S for stand): ")
                if choice.upper() == 'H':
                    time.sleep(0.5)
                    print("You chose to Hit")
                    userCards.append(deck.drawCard(userTotal))
                    userTotal = total(userCards)
                    print(f"\nThe Cards {user.user.capitalize()} have are: ")
                    for card in userCards:
                        card.show()
                        time.sleep(0.5)
                    print(f"\nThe total value of your card is {userTotal} points\n")
                    if bust(userTotal):
                        break
                else:
                    if dealerTotal < userTotal and dealerTotal < 17:
                        while True:
                            if dealerBust(dealerTotal):
                                time.sleep(1)
                                Player.deposit(user, (betAmt*2))
                                break
                            else:
                                if dealerTotal < userTotal and dealerTotal < 17:
                                    time.sleep(1)
                                    dealerCards.append(deck.drawCard(dealerTotal))
                                    print(f"The Cards Dealer have are: ")
                                    for card in dealerCards:
                                        card.show()
                                        time.sleep(0.5)
                                    dealerTotal = total(dealerCards)
                                    print(f"\nThe total value of dealer's card are {dealerTotal}.\n")
                                elif draw(dealerTotal, userTotal):
                                    time.sleep(1)
                                    for card in dealerCards:
                                        card.show()
                                        time.sleep(0.5)
                                    dealerTotal = total(dealerCards)
                                    print(f"\nThe total value of dealer's card are {dealerTotal}.\n")
                                    Player.deposit(user, betAmt)
                                    break
                                else:
                                    print("You've won the match!!")
                                    time.sleep(1)
                                    Player.deposit(user, (betAmt*2))
                                    break
                        break
                    elif draw(dealerTotal, userTotal):
                        time.sleep(1)
                        for card in dealerCards:
                            card.show()
                            time.sleep(0.5)
                        dealerTotal = total(dealerCards)
                        print(f"\nThe total value of dealer's card are {dealerTotal}.\n")
                        Player.deposit(user, betAmt)
                        break
                    else:
                        print("\nYou've won the match!!\n")
                        time.sleep(1)
                        Player.deposit(user, (betAmt*2))
                        break
        
        if replay():
            userCards.clear()
            count = 0
            continue
        else:
            break

def getUser():
    amount = 0
    name = ""
    while amount == 0:
            name = input("Please enter your name: ")
            amount = int(input("Please enter the amount you want to add to your wallet(in tenths position): $"))
    user = Player(name, amount)
    return user

def replay():
    response = input("Press Y to replay: ")
    if response.upper() == "Y" or response.upper() == "YES":
        return True
    return False

def total(cardList):
    total = 0
    for c in cardList:
        total += c.value
    return total

def bet(user):
    while True:
        amt = int(input("Choose your bet amount: $"))
        if amt <= user.balance:
            print(f"The amount you chose to bet is ${amt}.")
            time.sleep(0.5)
            Player.withDraw(user,amt)
            break
        else:
            print(f"The available balance in your wallet is {user.balance}")
            print("Please try again...")
            time.sleep(0.5)
            continue
    return amt
    
def bust(total):
    if total > 21:
        if 11 in userCards:
            for i in range(len(userCards)):
                if userCards[i] == 11:
                    userCards[i] == 1
                    return False
        time.sleep(1)
        print("You're bust, your point is above 21\n")
        time.sleep(0.5)
        print("You've lost your money\n")
        return True
    return False

def dealerBust(total):
    if total > 21:
        time.sleep(1)
        print("The dealer is bust, you won the game!!\n")
        time.sleep(0.75)
        print("Soon winning bonus will be credited to your BlackJack Wallet.\n")
        return True
    return False

def draw(dealer, user):
    if dealer == user:
        print("The match is draw!")
        return True
    return False


class Card:
    def __init__(self, name, value):
        self.suit = name
        self.value = value
    
    def show(self):
        print(f"{self.suit} of {self.value}")

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        
    def build(self):
        self.cards = []
        for s in ["Spades", "Diamonds", "Hearts", "Clubs"]:
            for v in range(1, 14):
                self.cards.append(Card(s, v))
    
    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
    
    def show(self):
        for c in self.cards:
            c.show()
    
    def drawCard(self, points):
        card = self.cards.pop()
        if card.value > 10:
            card.value = 10
        elif card.value == 1:
            if points < 11:
                card.value = 11
        return card

class Player:
    def __init__(self, name, balance = 0):
        self.user = name
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print(f"Amount of ${amount} is added, your current balance is ${self.balance}")
    
    def withDraw(self, amount):
        self.balance -= amount
        print(f"You've withdrawn ${amount}, the available balance in your wallet is ${self.balance}")


if __name__ == "__main__":
    main()