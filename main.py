from webserver import keep_alive
import os
import discord
from dotenv import load_dotenv
import random
import io
import pandas as pd
import bs4
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml

# variable definitions
all_abilities = {
    "POCKET DEADEYE": {
        "THROW UNDER PRESSURE": 80
    },
    "ROAMING DEADEYE": {
        "THROW ON THE RUN": 80
    },
	"FEARLESS": {
		"THROW UNDER PRESSURE": 90
	},
	"SET FEET LEAD": {
		"THROW POWER": 90
	},
	"PASS LEAD ELITE": {
		"THROW POWER": 90,
		"SHORT ACCURACY": 85,
		"MEDIUM ACCURACY": 85,
		"DEEP ACCURACY": 85
	},
	"GUNSLINGER": {
		"THROW POWER": 94
	},
	"ESCAPE ARTIST": {
		"SPEED": 85,
		"ACCELERATION": 87
	},
	"HOT ROUTE MASTER": {
		"AWARENESS": 90
	},
	"DASHING DEADEYE": {
		"THROW ON THE RUN": 90
	},
	"BULLDOZER": {
		"STRENGTH": 83,
		"TRUCKING": 83
	},
	"TANK": {
		"STRENGTH": 83,
		"BREAK TACKLE": 85
	},
	"ARM BAR": {
		"STRENGTH": 85,
		"STIFF ARM": 90
	},
	"BACKFIELD MISMATCH": {
		"CATCHING": 75,
		"SHORT ROUTE RUNNING": 80
	},
	"MATCHUP NIGHTMARE": {
		"SHORT ROUTE RUNNING": 75
	},
	"FREIGHT TRAIN": {
		"STRENGTH": 85,
		"BREAK TACKLE": 92,
		"TRUCKING": 90,
		"STIFF ARM": 90
	},
	"ROUTE APPRENTICE": {
		"SHORT ROUTE RUNNING": 85,
		"MED ROUTE RUNNING": 85,
		"DEEP ROUTE RUNNING": 85
	},
	"ROUTE TECHNICIAN": {
		"SHORT ROUTE RUNNING": 90,
		"MED ROUTE RUNNING": 90,
		"DEEP ROUTE RUNNING": 90
	},
	"SLOT O MATIC": {
		"CATCHING": 90,
		"SHORT ROUTE RUNNING": 90
	},
	"DEEP OUT ELITE": {
		"CATCH IN TRAFFIC": 90,
		"RELEASE": 90,
		"JUMP": 85
	},
	"RED ZONE THREAT": {
		"CATCH IN TRAFFIC": 90,
		"SPECTACULAR CATCH": 85,
		"SHORT ROUTE RUNNING": 90,
		"MED ROUTE RUNNING": 90
	},
	"TE APPRENTICE": {
		"SHORT ROUTE RUNNING": 85,
		"MED ROUTE RUNNING": 85,
		"DEEP ROUTE RUNNING": 85
	},
	"EDGE PROTECTOR": {
		"PASS BLOCK": 90
	},
	"NO OUTSIDERS": {
		"AWARENESS": 85,
		"BLOCK SHED": 88
	},
	"SECURE TACKLER": {
		"TACKLING": 90
	},
	"EDGE THREAT": {
		"SPEED": 84,
		"FINESSE MOVE": 92
	},
	"DOUBLE OR NOTHING": {
		"STRENGTH": 88,
		"POWER MOVE": 92
	},
	"INSIDE STUFF": {
		"AWARENESS": 85,
		"BLOCK SHED": 88
	},
	"MID ZONE KO": {
		"AWARENESS": 85,
		"ZONE COVERAGE": 90
	},
	"LURKER": {
		"JUMP": 85,
		"CATCH": 85
	},
	"ACROBAT": {
		"AWARENESS": 85,
		"PLAY RECOGNITION": 85,
		"JUMP": 85
	},
	"ONE STEP AHEAD": {
		"AWARENESS": 90,
		"PLAY RECOGNITION": 85,
		"MAN COVERAGE": 90
	}
	
	
}
striker_id = "471794438515982336"
mee6_id = "159985870458322944"
bot_id = "964612844937183312"

eagles_hate_matrix = [
    ["Someone mentioned the Eagles?", "https://tenor.com/view/eagles-suck-pats-philly-gif-10982340"],
    ["Imagine being an Eagles fan.", "https://tenor.com/view/eagles-suck-gif-10644010"],
    ["Griddy if you suck!", "https://tenor.com/view/hurts-gif-23436656"],
    ["You could've had this guy but you got Jalen Reagor.", "https://tenor.com/view/nfl-football-griddy-gif-gif-25216449"]
]
eagles_hate_options = len(eagles_hate_matrix)

zone_quotes = ["Look at my 95% completion percentage - KJ",
               "Rules? What are those? - Ben",
               ["Whatever the fuck this was:", "https://cdn.discordapp.com/attachments/768835530665492503/919198738893918238/Screenshot_20211211-0706492.png"], 
["https://cdn.discordapp.com/attachments/768835530665492503/908159497929908254/unknown.png", " - Shalton"],
               "Thats fucking football right there. None of that pansy ass dick tugging smile for the camera bullshit. Men puke, men poop on the field, men deliver their new born baby on the side lines. Fucking hard core dick in the ass butterball foosball fuck it chuck it game time shit. Take it to the showers. Dicks get shoved in places you don’t even remember. We win together we celebrate together. Football is back baby. - Jazz",
["https://cdn.discordapp.com/attachments/768835530665492503/818893098620420126/unknown.png", " - Scotty Foisy :goat:"],
			   "what lg - TGroves22"
]

fuck_mee6_message = f"Did someone say MEE6? Fuck <@{mee6_id}>."

rules_activations = ["rules", "!rules", "!rulebook"]
superbowl_activations = ["super bowls", "!superbowl", "!superbowls", "!bowl"]
playercheck_activations = ["!playercheck", "!abilitycheck", "playercheck", "abilitycheck"]
tbearbutler_activations = ["tbear", "butler", "!tbear", "!butler"]
recordbook_activations = ["!record", "!records", "!recordbook", "!history", "record", "records", "recordbook"]

# testing attributes function
def testAttributes(needs, test):  # testing attributes function
    for keys in needs.keys():
        if needs[keys] > int(test[keys][0]):
            return "Your player **does not** qualify. His " + keys.lower(
            ).capitalize() + " is too low. It must be atleast " + str(
                needs[keys]) + " but it's only " + str(
                    test[keys][0]) + ". You may enter another ability or end. "
    return "Your player **qualifies** assuming he is in the correct position. You may enter another ability or end."


#building stuff
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()


@client.event
async def on_message(message):
    sender_id = message.author.id
    if str(sender_id) != bot_id:
        channel = message.channel
        # indent everything
        if message.content.lower() in playercheck_activations:
            await channel.send('What is your players NeonSportz URL?')
    
            def check(m): #check function for messages
                return m.channel == channel
    
            msg = await client.wait_for('message', check=check)
          
            print(msg.content)
            
            if "https" != msg.content.split(":")[0]:  # checking if URL is valid
                await channel.send(
                    "This link is invalid. Try again or type something to terminate."
                )
                msg = await client.wait_for('message', check=check)
    
            check_ability = True  # makes sure they entered a valid URL
    
            if "https" != msg.content.split(":")[0]:
                check_ability = False  # checking if URL is valid again, else quit
    
            html = urlopen(msg.content)
            soup = BeautifulSoup(html, 'html.parser')
            total_stats = pd.DataFrame()
    
            for i in range(5, 13):  # scraping website for player stats
                current = soup.find_all("table")[i]
                current_frame = pd.read_html(str(current))[0]
                current_frame = current_frame.iloc[1:]
                total_stats = pd.concat([total_stats, current_frame])
            total_stats.columns = ["Attribute", "Value"]
            total_stats = total_stats.set_index("Attribute").T.to_dict("list")
    
            counter = 0  # counter for failed attempts of abilities --> 2 and it quits
            time = 0
    
            while check_ability == True:  # this is where the actual ability testing starts
                if time == 0:
                    await channel.send(
                        'What ability do you want to check? Type "all" to see the checkable abilities. Type "end" to quit.'
                    )
                    time = 1
                ability_test = await client.wait_for('message')
    
                if counter == 1:  # 2 failed attempts
                    await channel.send(
                        "Your request has ended due to invalid ability names. You may start again if you would like."
                    )
                    break
                elif ability_test.content == "all":  # they want to see all abilities
                    ability_checker_list = ""
                    for key in all_abilities.keys():
                        ability_checker_list += "| " + key.lower().title(
                        ) + " "
                    await channel.send("Here is a list: " + ability_checker_list +
                                       " | Please enter an ability. ")
                elif ability_test.content == "end":  # they want to end
                    await channel.send("You ended. Talk again soon!")
                    break
                elif ability_test.content.upper() not in all_abilities.keys(
                ):  # they didn't enter a valid ability
                    await channel.send(
                        "That is **not a valid ability**. Please recheck spelling and enter an ability again. "
                    )
                    counter = counter + 1
                else:  # they entered a valid ability
                    await channel.send(
                        testAttributes(all_abilities[ability_test.content.upper()],
                                       total_stats))
    
        if message.content.lower().startswith('striker'): await channel.send(f'Did someone say Striker? Hey sexy <@{striker_id}>')	
        if (message.content.lower() in tbearbutler_activations) and message.content != "TBear and Butler:":
            await channel.send("TBear and Butler:")
            await channel.send("https://tenor.com/view/kiss-make-out-gay-tongue-kiss-french-kiss-gif-17654914")
    
        if message.content.lower().startswith('eagles'):
            
            eagles_message_number = random.randint(0,eagles_hate_options-1)
            
            await channel.send(eagles_hate_matrix[eagles_message_number][0])
            await channel.send(eagles_hate_matrix[eagles_message_number][1])
    
        if message.content.lower() in rules_activations:  # rule book command
            await channel.send("Look at the rule book ya fucking cheeser: https://docs.google.com/document/d/1VQKD080B3SC_rQorGGDi3WO2hXSa3Osz0dfDz6_RitM/edit#heading=h.iownh1y6rxey")
        
        if message.content.lower() in recordbook_activations: # record book command
            await channel.send("Shoutout to Swan for the best Zone record book: https://docs.google.com/spreadsheets/d/1zGq4IeWtQkSs-LsB1NIZXlFVebDQ7Oht/edit?usp=sharing&ouid=109230297152532277681&rtpof=true&sd=true")
        
        
        if "mee6" in message.content.lower() and message.content != fuck_mee6_message: # mee6 sucks
            await channel.send(fuck_mee6_message)
        
        
        if mee6_id == str(sender_id): # mee6 talks
            await channel.send(f"Shut the fuck up <@{mee6_id}>. Only one bot can rule this place.")
        
        
        if message.content.lower() in superbowl_activations: # super bowl command (mainly to flex that I've won 2)
            await channel.send("Madden 22 Super Bowl I: tylxr | Super Bowl II: tylxr | Super Bowl III: Moe | Super Bowl IV: Henry")
        
        
        if message.content.lower().startswith("trey"): # trey lance
            await channel.send("The Future is **here**.")
            await channel.send("https://tenor.com/view/trey-lance-49ers-trey-trey-area-san-francisco49ers-gif-24843547")
        
        
        if "goat" in message.content.lower(): # lebron (the goat)
            await channel.send("Did someone mention the GOAT?")
            await channel.send("https://tenor.com/view/lebron-james-game6-miami-heat-gif-16098081")
    
        if message.content.lower().startswith("!quote") or message.content.lower().startswith("!zonequote"):
            quote_number = random.randint(0,len(zone_quotes)-1)
            if isinstance(zone_quotes[quote_number], str):
                await channel.send(zone_quotes[quote_number])
            else:
                await channel.send(zone_quotes[quote_number][0])
                await channel.send(zone_quotes[quote_number][1])

    
keep_alive()  # end of program

TOKEN = os.environ.get("DISCORD_BOT_SECRET")

client.run(TOKEN)
