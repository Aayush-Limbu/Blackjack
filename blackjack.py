from random import randint

class Blackjack(object):
    uservalue = 0
    dealervalue = 0

    def randomint(self):
        return randint(1,13)
        
    def add(self):
        a = self.randomint()
        b = self.randomint()
        self.name(a)
        self.name(b)
        a = self.value(a)
        b = self.value(b)
        return a+b

    def check(self, val, num):
        if val == 'y' or val == 'n':
          return val
        else:
          print("Sorry I didn't get that.")
          val = input(f'You have {num}. Hit (y/n)? ')
          return self.check(val, num)

    
    def name(self, card_rank):
        if card_rank == 1:
            card_name = "Ace"
        elif card_rank == 11:
            card_name = "Jack"
        elif card_rank == 12:
            card_name = "Queen"
        elif card_rank == 13:
            card_name = "King"
        else:
            card_name = str(card_rank)

        if card_rank == 1 or card_rank == 8:
            drew_prefix = 'Drew an '
        else:
            drew_prefix = 'Drew a '

        print(drew_prefix + card_name)

    def value(self, card_rank):
        if card_rank == 11 or card_rank == 12 or card_rank == 13:
            card_value = 10
        elif card_rank == 1:
            card_value = 11
        else:
            card_value = card_rank

        return card_value
    
    def usersum(self, hand_sum):
        if hand_sum == 21:
            print(f'Final hand: {hand_sum}.')
            print('BLACKJACK!')
        elif hand_sum > 21:
            print(f'Final hand: {hand_sum}.')
            print("BUST.")
        else:
            val = input(f'You have {hand_sum}. Hit (y/n)? ')
            if self.check(val, hand_sum) == 'y':
              z = self.randomint()
              self.name(z)
              z = self.value(z)
              hand_sum += z
              self.uservalue = hand_sum
              self.usersum(hand_sum)
            else:
              print(f'Final hand: {hand_sum}.')
              self.uservalue = hand_sum
        

    def dealersum(self, hand_sum):
        if hand_sum == 21:
            print(f'Final hand: {hand_sum}.')
            print('BLACKJACK!')
        elif hand_sum > 21:
            print(f'Final hand: {hand_sum}.')
            print("BUST.")
        elif hand_sum >= 17:  
            print(f'Final hand: {hand_sum}.')
        else:
            print(f'Dealer has {hand_sum}.')
            card = self.randomint()
            self.name(card)
            card_value = self.value(card)
            hand_sum += card_value
            self.dealersum(hand_sum)
        self.dealervalue = hand_sum

    
blackjack = Blackjack()

print('-----------\nYOUR TURN\n-----------')

blackjack.usersum(blackjack.add())

print('-----------\nDEALER TURN\n-----------')

blackjack.dealersum(blackjack.add())

print('-----------\nGAME RESULT\n-----------')

if blackjack.uservalue < 22:
    if blackjack.dealervalue > 21:
        print("You win!")
    elif blackjack.uservalue == blackjack.dealervalue:
        print("Push.")
    elif blackjack.uservalue > blackjack.dealervalue:
        print("You win!")
    else:
        print("Dealer wins!")
else:
    print("Dealer wins!")

