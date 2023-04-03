import random


# Define the possible suits and ranks of a deck of cards
suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Define the values of each rank
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': [1, 11]}

# Define the possible actions a player can take in a game of blackjack
actions = ['Hit', 'Stick']

def get_hand_total(hand):
    """Returns the total value of a hand of cards."""
    total = 0
    num_aces = 0
    for card in hand:
        rank = card[1]
        if rank == 'Ace':
            num_aces += 1
        else:
            total += values[rank]

    # Add the value of the Aces to the total, taking into account their dual value
    for i in range(num_aces):
        if total + 11 > 21:
            total += 1
        else:
            total += 11

    return total

def monte_carlo_action(player_hand, dealer_hand, deck):
    """Returns the optimal action for the player to take based on the Monte Carlo method."""
    player_total = get_hand_total(player_hand)
    dealer_total = get_hand_total(dealer_hand)
    if player_total >= 17:
        # Stick if the player has 17 or more points
        return 'Stick'
    else:
        # Hit if the player has less than 17 points
        return 'Hit'

# Define the Monte Carlo method for simulating a game of blackjack
def monte_carlo(num_simulations):
    # Initialize counters for wins, losses, and draws
    wins = 0
    losses = 0
    draws = 0

    # Loop through the specified number of simulations
    for i in range(num_simulations):
        # Create a new deck of cards and shuffle it
        deck = []
        for suit in suits:
            for rank in ranks:
                deck.append((suit, rank))
        random.shuffle(deck)

        # Deal the first two cards to the player and the dealer
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        # Check if the player has blackjack (21 points on the first two cards)
        player_total = get_hand_total(player_hand)
        if player_total == 21:
            # The player wins if they have blackjack
            wins += 1
            print("Simulation #{}: Player wins with blackjack!".format(i+1))
            continue

        # If the player doesn't have blackjack, play out the hand by taking actions until the player sticks or busts
        while True:
            # Check if the player should hit or stick based on the Monte Carlo method
            action = monte_carlo_action(player_hand, dealer_hand, deck)
            if action == 'Stick':
                break
            else:
                # Hit: add a new card to the player's hand
                player_hand.append(deck.pop())
                player_total = get_hand_total(player_hand)
                if player_total > 21:
                    # The player busts and loses the game
                    losses += 1
                    print("Simulation #{}: Player loses, busts!".format(i+1))
                    break

        # If the player didn't bust, play out the dealer's hand
        if player_total <= 21:
            dealer_total = get_hand_total(dealer_hand)
            while dealer_total < 17:
                # The dealer hits on 16 or lower
                dealer_hand.append(deck.pop())
                dealer_total = get_hand_total(dealer_hand)

             # Determine the winner of the game based on the player and dealer's final hand totals
            if dealer_total > 21:
                # The dealer bust and the player wins
                wins += 1
                print("Simulation #{}: Player wins, dealer busts!".format(i+1))
            elif dealer_total > player_total:
                # The dealer wins
                losses += 1
                print("Simulation #{}: Player loses, dealer wins!".format(i+1))
            elif dealer_total == player_total:
                # It's a draw
                draws += 1
                print("Simulation #{}: Draw!".format(i+1))
            else:
                # The player wins
                wins += 1
                print("Simulation #{}: Player wins!".format(i+1))

        # Print the final results of the simulations
        print("Simulation complete! Wins: {}, Losses: {}, Draws: {}".format(wins, losses, draws))