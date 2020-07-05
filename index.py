from selenium import webdriver
browser = webdriver.Safari()
browser.get('https://web.whatsapp.com')
from bs4 import BeautifulSoup
import requests
from time import sleep
from selenium.webdriver.common.keys import Keys
import json
from googletrans import Translator
translator = Translator()
from datetime import datetime
from random import randint

def send(text):
    textarea = browser.find_elements_by_class_name("_3u328")[1]
    textarea.send_keys(text)
    sendBtn = browser.find_element_by_class_name("_3M-N-")
    sendBtn.send_keys(Keys.RETURN)

def calc(arg):
    solution = str(eval(arg))
    solutionMessage = "Dein Ergebnis für die Aufgabe " + arg + " ist " + solution
    send(solutionMessage)

def corona():
    global response

    response = requests.post("Enter your WrapAPIlink", json={
      "wrapAPIKey": "APIKey"
    })
    response = response.json()
    response = response["data"]
    response = response["output"]

def trans(arg):
    print(arg)
    if(arg.startswith("de")):
        arg = arg.replace("de ", "")
        send("Original: " + arg + "\nDeutsch: " + str(translator.translate(arg, dest='de').text))
    elif(arg.startswith("en")):
        arg = arg.replace("en ", "")
        send("Original: " + arg + "\nEnglisch: " + str(translator.translate(arg, dest='en').text))
    elif(arg.startswith("fr")):
        arg = arg.replace("fr ", "")
        send("Original: " + arg + "\nFranzösisch: " + str(translator.translate(arg, dest='en').text))
    else:
        send("Diese Sprache kann ich noch nicht.")

def ssp(arg):
    random = randint(1, 3)
    # 1: Schere, 2: Stein, 3: Papier
    if(arg.upper() == "SCHERE" or arg.upper() == "STEIN" or arg.upper() == "PAPIER"):
        if(random == 1):
            if(arg.upper() == "SCHERE"):
                send("Unentschieden! Ich hatten auch Schere.")
            elif(arg.upper() == "STEIN"):
                send("Du hast gewonnen! Ich hatte Schere.")
            elif(arg.upper() == "PAPIER"):
                send("Du hast verloren! Ich hatte Schere.")
        elif(random == 2):
            if(arg.upper() == "SCHERE"):
                send("Du hast verloren! Ich hatte Stein.")
            elif(arg.upper() == "STEIN"):
                send("Unentschieden! Ich hatten auch Stein.")
            elif(arg.upper() == "PAPIER"):
                send("Du hast gewonnen! Ich hatte Stein.")
        elif(random == 3):
            if(arg.upper() == "SCHERE"):
                send("Du hast gewonnen! Ich hatte Papier.")
            elif(arg.upper() == "STEIN"):
                send("Du hast verloren! Ich hatte Papier.")
            elif(arg.upper() == "PAPIER"):
                send("Unentschieden! Ich hatten auch Papier.")
    else:
        return send("Bitte schreibe Schere, Stein oder Papier nach /ssp")


while True:
    unread = browser.find_elements_by_class_name("P6z4j") # The green dot tells us that the message is new
    name,message  = '',''
    if len(unread) > 0:
        ele = unread[-1]
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(ele, 0, -20) # move a bit to the left from the green dot

        # Clicking couple of times because sometimes whatsapp web responds after two clicks
        try:
            action.click()
            action.perform()
            action.click()
            action.perform()
            action.click()
            action.perform()
        except Exception as e:
            pass
        try:
            name = browser.find_element_by_class_name("_19RFN").text  # Contact name
            message = browser.find_elements_by_class_name("_F7Vk")[-1]  # the message content
            message = message.text.lower()
            # if '/corona' in message.text.lower():
            #     send("Moin")
            if message.startswith('/calc '):
                calc(message.replace("/calc ", ""))
            if message == "/corona":
                corona()
                send("Infizierte: " + response[0] + "\nTote: " + response[1] + "\nWiederhergestellte: " + response[2])
            if(message.startswith('/trans')):
                trans(message.replace("/trans ", ""))
            if(message == "/help"):
                send("Aktuelle Befehle:\n/help\n   Zeigt alle Befehle an\n/next\n   Zeigt an, was man in der nächsten Stunde hat.\n/calc <Aufgabe>\n   Taschenrechner Plus: + ,  Minus: - ,  Mal: * ,  Geteiltdurch: /\n/trans <Zielsprache> <Text>\n   Übersetzt deinen Text in Deutsch, Englisch oder Französisch.\n   Nach Deutsch: de\n   Nach Englsich: en\n   Nach Französisch: fr\n/ssp <Schere/Stein/Papier>\n   Spiele Schere, Stein oder Papier.")
            if(message.startswith("/ssp")):
                ssp(message.replace("/ssp ", ""))

            # Go to default Account
            textarea = browser.find_element_by_class_name("_3u328")
            textarea.send_keys("Marc-Aurel")
            textarea.send_keys(Keys.ENTER)
        except Exception as e:
            print(e)
            pass
    sleep(2) # A 2 second pause so that the program doesn't run too fast
