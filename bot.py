import discord
import random
from mytoken import discordToken

intents = discord.Intents.default()
intents.message_content = True
game_in_progress = False
split = False
 
actionno = 0

client = discord.Client(intents=intents)

# Define the set of cards
cards = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
deck = [f"{card} of {suit}" for card in cards for suit in suits]

# Create a dictionary to store player information
player = {"name": "", "hand": [], "score": 0, "active": True}

player1 = {"name": "", "hand": [], "score": 0, "active": False}
player2 = {"name": "", "hand": [], "score": 0, "active": False}

# Create a dictionary to store dealer information
dealer = {"name": "Dealer", "hand": [], "score": 0, "active": True}

# Define the reset function to set the deck back to its original order
def reset():
    global deck
    global player
    global player1
    global player2
    global dealer
    global split
    split = False
    deck = [f"{card} of {suit}" for card in cards for suit in suits]
    player = {"name": "", "hand": [], "score": 0, "active": True}
    player1 = {"name": "", "hand": [], "score": 0, "active": False}
    player2 = {"name": "", "hand": [], "score": 0, "active": False}
    dealer = {"name": "Dealer", "hand": [], "score": 0, "active": True}

# Define the shuffle function to shuffle the deck
def shuffle():
    global deck
    random.shuffle(deck)

def calcPlayerScore():
    global player
    global player1    
    global player2
    score = 0
    noOfAces = 0
    for x in player["hand"]:
        if(x.startswith("Ace")):
            score += 1
            noOfAces+=1
        elif(x.startswith("Jack")):
            score += 10
        elif(x.startswith("Queen")):
            score += 10
        elif(x.startswith("King")):
            score += 10
        elif(x.startswith("10")):
            score += 10
        else:
            score += int(x[0])
    while(score <= 11 and noOfAces>0):
        score += 10
        noOfAces-=1
    player['score'] = score

    if(player1["active"]):
        score1 = 0
        noOfAces1 = 0
        for x in player1["hand"]:
            if(x.startswith("Ace")):
                score1 += 1
                noOfAces1+=1
            elif(x.startswith("Jack")):
                score1 += 10
            elif(x.startswith("Queen")):
                score1 += 10
            elif(x.startswith("King")):
                score1 += 10
            elif(x.startswith("10")):
                score1 += 10
            else:
                score1 += int(x[0])
        while(score1 <= 11 and noOfAces1>0):
            score1 += 10
            noOfAces1-=1
        player1['score'] = score1

    if(player2["active"]):
        score2 = 0
        noOfAces2 = 0
        for x in player2["hand"]:
            if(x.startswith("Ace")):
                score2 += 1
                noOfAces2+=1
            elif(x.startswith("Jack")):
                score2 += 10
            elif(x.startswith("Queen")):
                score2 += 10
            elif(x.startswith("King")):
                score2 += 10
            elif(x.startswith("10")):
                score2 += 10
            else:
                score2 += int(x[0])
        while(score2 <= 11 and noOfAces2>0):
            score2 += 10
            noOfAces2-=1
        player2['score'] = score2

def calcDealerScore():
    global dealer
    score = 0
    noOfAces = 0
    for x in dealer["hand"]:
        if(x.startswith("Ace")):
            score += 1
            noOfAces+=1
        elif(x.startswith("Jack")):
            score += 10
        elif(x.startswith("Queen")):
            score += 10
        elif(x.startswith("King")):
            score += 10
        elif(x.startswith("10")):
            score += 10
        else:
            score += int(x[0])
    while(score <= 11 and noOfAces>0):
        score += 10
        noOfAces-=1
    dealer['score'] = score


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name="Kızların duygularıyla"))

@client.event
async def on_message(message):
    global game_in_progress
    if message.author == client.user:
        return

    if message.content.startswith('help'):
        await message.channel.send('This is a simple blackjack bot. Your aim is to score higher than the dealer and lower than 21. The dealer will draw until their score is at least 17')
        await message.channel.send('!newgame to start the game\n!hit to hit\n!stand to stand\n!split to split your hand in the first round\n!hit1, !hit2 to hit after split\n!stand1, !stand2 to stand after split')
        await message.channel.send('You can split even if your two cards aren\'t the same value.\nAfter the game finishes you must use !newgame to shuffle the deck and restart\nThe deck of this game has 52 cards.')    
    if message.content.startswith('!newgame'):
        if game_in_progress:
            await message.channel.send("A game is already in progress. Please wait for it to finish or use !finishgame to end it prematurely.")
            return
        reset()
        shuffle()

        game_in_progress = True
        player["name"] = message.author.name
        player["hand"].append(deck.pop())
        player["hand"].append(deck.pop())
        dealer["hand"].append(deck.pop())
        dealer["hand"].append(deck.pop())
        calcPlayerScore()
        await message.channel.send("A new game has started.")
        await message.channel.send(f"{player['name']}, your current hand is {player['hand']} your score is {player['score']}")
        await message.channel.send(f"Dealer's shown card is {dealer['hand'][0]}")
        if(player["score"]==21):
            await message.channel.send(f"{player['name']} wins with a natural 21")
            game_in_progress = False
            return
        await message.channel.send("Type !hit to draw a card or !stand to keep your current hand or !split to split")

    


    if message.content.startswith('!split'):
 
        global split
        if not game_in_progress:
            await message.channel.send("No game is in progress. Please start a new game with !newgame")
            return
        if message.author.name != player["name"]:
            await message.channel.send("It is not your turn")
            return
        if split:
            await message.channel.send("You have already splitted")
            return
        player1["name"] = player["name"]
        player1["hand"].append(player["hand"].pop(0))
        player1["active"] = True
        player2["name"] = player["name"]
        player2["hand"].append(player["hand"].pop(0))
        player2["active"] = True
        player["active"] = False
        player["hand"] = []
        player["score"] = 0
        calcPlayerScore()
        await message.channel.send(f"{player1['name']}'s first hand: {player1['hand']}")
        await message.channel.send(f"{player2['name']}'s second hand: {player2['hand']}")
        await message.channel.send("Type !hit1 to draw a card for first hand or !stand1 to keep your current hand for first hand")
        await message.channel.send("Type !hit2 to draw a card for second hand or !stand2 to keep your current hand for second hand")
 
        split = True
        
    if message.content.startswith('!hit1'):
        
        if not game_in_progress:
            await message.channel.send("No game is in progress. Please start a new game with !newgame")
            return
        if message.author.name != player["name"]:
            await message.channel.send("It is not your turn")
            return
        if not split:
            await message.channel.send("You have not splitted")
            return
        card = deck.pop()
        player1["hand"].append(card)
        calcPlayerScore()
        score = player1["score"]
        await message.channel.send(f'{player1["name"]}, your new hand is {player1["hand"]}, your score is {score}')
        if score == 21:
            await message.channel.send(f'{player1["name"]}, your score is 21. You win.')
            player1["active"] = False
            player1["score"] = score
            game_in_progress = False
            return
        if score > 21:
            await message.channel.send(f'{player1["name"]}, your score is {score}. Game is not over, please try your other hand')
            player1["active"] = False
            player1["score"] = score
            #game_in_progress = False
            return

        await message.channel.send("Type !hit1 to draw another card or !stand1 to keep your current hand")
        return

    if message.content.startswith('!hit2'):
 
        if not game_in_progress:
            await message.channel.send("No game is in progress. Please start a new game with !newgame")
            return
        if message.author.name != player["name"]:
            await message.channel.send("It is not your turn")
            return
        if not split:
            await message.channel.send("You have not splitted")
            return
        if player1["active"]:
            await message.channel.send("Please hit your hand 1 first")
            return
        card = deck.pop()
        player2["hand"].append(card)
        calcPlayerScore()
        score = player2["score"]
        await message.channel.send(f'{player2["name"]}, your new hand is {player2["hand"]}, your score is {score}')
        if score == 21:
            await message.channel.send(f'{player2["name"]}, your score is 21. You win.')
            player2["active"] = False
            player2["score"] = score
            game_in_progress = False
            return
        if score > 21:
            calcDealerScore()
            if(player1["score"]>21):
                await message.channel.send(f'{player2["name"]}, your first hand is {player1["hand"]} with a score {player1["score"]}.')
                await message.channel.send(f'{player2["name"]}, your second hand is {player2["hand"]} with a score {player2["score"]}. You lose.')
            if(player1["score"]<21):
                while(dealer["score"] < 17):
                    card = deck.pop()
                    dealer["hand"].append(card)
                    calcDealerScore()
                    await message.channel.send(f"Dealer's new hand is {dealer['hand']} with a score of {dealer['score']}")
                await message.channel.send(f"Dealer's final hand is {dealer['hand']} with a score of {dealer['score']}")
                if(dealer["score"]>21):
                    await message.channel.send(f"Dealer busts, {player1['name']} wins with the first hand with a score of {player1['score']}!")
                elif(dealer["score"]==21):
                    await message.channel.send(f"Dealer wins with a score of {dealer['score']}.\nYour first hand is: {player1['hand']}.\nYour second hand is: {player2['hand']}.")
                elif(player1["score"]>dealer["score"]):
                    await message.channel.send(f"{player1['name']} wins with the first hand with a score of {player1['score']}!")
                else:
                    await message.channel.send(f"Dealer wins with a score of {dealer['score']}.\nYour first hand is: {player1['hand']}.\nYour second hand is: {player2['hand']}.")
            player2["active"] = False
            player2["score"] = score
            game_in_progress = False
            return
        
        await message.channel.send("Type !hit2 to draw another card or !stand2 to keep your current hand")
        return

    if message.content.startswith('!hit'):
 
        if not game_in_progress:
            await message.channel.send("No game is in progress. Please start a new game with !newgame")
            return
        if message.author.name != player["name"]:
            await message.channel.send("It is not your turn")
            return
        if split:
            await message.channel.send("You have splitted use !hit1 or !hit2 instead")
            return
        card = deck.pop()
        player["hand"].append(card)
        calcPlayerScore()
        score = player["score"]
        await message.channel.send(f'{player["name"]}, your new hand is {player["hand"]}, your score is {score}')       
        if score == 21:
            await message.channel.send(f'{player["name"]}, your hand is {player["hand"]}, your score is 21. You win.')
            player["active"] = False
            player["score"] = score
            game_in_progress = False
            return
        if score > 21:
            await message.channel.send(f'{player["name"]}, your hand is {player["hand"]}, your score is {player["score"]}. You lose.')
            player["active"] = False
            player["score"] = score
            game_in_progress = False
            return

        await message.channel.send("Type !hit to draw another card or !stand to keep your current hand")

    if message.content.startswith('!stand1'):
        if not game_in_progress:
            await message.channel.send("No game is in progress. Please start a new game with !newgame")
            return
        if message.author.name != player["name"]:
            await message.channel.send("It is not your turn")
            return
        if not split:
            await message.channel.send("You have not splitted")
            return
        player1["active"] = False
        
        await message.channel.send(f"You have stood on your first hand. Dealer will not draw cards until your other hand is finished")
        await message.channel.send(f"To remind you, your second hand was {player2['hand']}")
        return

    if message.content.startswith('!stand2'):
        if not game_in_progress:
            await message.channel.send("No game is in progress. Please start a new game with !newgame")
            return
        if message.author.name != player["name"]:
            await message.channel.send("It is not your turn")
            return
        if not split:
            await message.channel.send("You have not splitted")
            return
        if player1["active"]:
            await message.channel.send("Please stand on your hand 1 first")
            return
        player2["active"] = False
        calcDealerScore()
        dealer_score = dealer["score"]
        await message.channel.send(f"Dealer's hand was {dealer['hand']} with a score of {dealer_score}")
        while(dealer_score < 17):
            card = deck.pop()
            dealer["hand"].append(card)
            calcDealerScore()
            dealer_score = dealer["score"]
            await message.channel.send(f"Dealer's new hand is {dealer['hand']} with a score of {dealer_score}")

        await message.channel.send(f"Dealer's final hand is {dealer['hand']} with a score of {dealer_score}")
        if dealer_score > 21:
            await message.channel.send(f"Dealer busts, {player2['name']} wins with the second hand with a score of {player2['score']}!")
            game_in_progress = False
            return
        if player2["score"] == 21:
            await message.channel.send(f"{player2['name']} wins with the second hand with a score of 21!")
            game_in_progress = False
            return
        if player1["score"] == 21:
            await message.channel.send(f"{player2['name']} wins with the first hand with a score of 21!")
            game_in_progress = False
            return
        if player2["score"] > dealer_score and player2["score"] < 21:
            await message.channel.send(f"{player2['name']} wins with the second hand with a score of {player2['score']}")
            game_in_progress = False
            return
        if player1["score"] > dealer_score and player1["score"] < 21:
            await message.channel.send(f"{player2['name']} wins with the first hand with a score of {player1['score']}")
            game_in_progress = False
            return
        if  player2["score"] <= dealer_score and dealer_score == player1["score"]:
            await message.channel.send("It's a tie!")
            game_in_progress = False
            return
        if player1["score"] <= dealer_score and dealer_score == player2["score"]:
            await message.channel.send("It's a tie!")
            game_in_progress = False
            return
        else:
            await message.channel.send(f"Dealer wins with a score of {dealer_score}.\nYour first hand is: {player1['hand']}.\nYour second hand is: {player2['hand']}.")
            game_in_progress = False
            return

    if message.content.startswith('!stand'):
        if not game_in_progress:
            await message.channel.send("No game is in progress. Please start a new game with !newgame")
            return
        if message.author.name != player["name"]:
            await message.channel.send("It is not your turn")
            return
        if split:
            await message.channel.send("You have splitted use !stand1 or !stand2 instead")
            return
        player["active"] = False
        calcDealerScore()
        dealer_score = dealer["score"]
        await message.channel.send(f"Dealer's hand was {dealer['hand']} with a score of {dealer_score}")
        while(dealer_score < 17):
            card = deck.pop()
            dealer["hand"].append(card)
            calcDealerScore()
            dealer_score = dealer["score"]
            await message.channel.send(f"Dealer's new hand is {dealer['hand']} with a score of {dealer_score}")

        await message.channel.send(f"Dealer's final hand is {dealer['hand']} with a score of {dealer_score}")
        if dealer_score > 21:
            await message.channel.send(f"Dealer busts, {player['name']} wins!")
            game_in_progress = False
            return
        if dealer_score > player["score"]:
            await message.channel.send(f"Dealer wins with a score of {dealer_score}")
            game_in_progress = False
            return
        if dealer_score < player["score"]:
            await message.channel.send(f"{player['name']} wins with a score of {player['score']}")
            game_in_progress = False
            return
        if dealer_score == player["score"]:
            await message.channel.send("It's a tie!")
            game_in_progress = False
            return
 
        
client.run(discordToken)


    