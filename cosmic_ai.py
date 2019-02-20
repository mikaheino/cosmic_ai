# Cosmic AI
# pääkonttorin_säbä -Slack integration
# Mika Heino, 21.10.2018
#
# CHANGE HISTORY
# 23.10.2018
# -> channel to here
# -> replace(players[:1]) to replace(players[:2]) for allowing player number to higher than 9
# -> added more info about event cancellation and about deadlines
# -> / Mika
# 25.10.2018
# -> added event parsing, if event contains some text in Description -field, it get's messed up
# -> added printing about reservation cancelling
# -> / Mika
# 14.01.2019
# -> changed text on notifications to remove friday event


import pandas as pd
import random as random
import arrow

def lambda_handler(event, context):
    list_of_events="https://paakonttori.nimenhuuto.com/calendar/csv"
    # Luetaan urlista lista eventeistä
    eventdata = pd.read_csv(list_of_events)
    # Haetaan seuraavaksi uusimman tapahtuman event-url datasta arvoon c

    # Jos eventtiin on lisätty jotain ylimääräistä tekstiä, tulee se sijottaa seuraavaan replace funktioon korvattava teksti
    latest_event = eventdata['Description'].iloc[0].replace('Säbää ja länkytystä', '').strip()
    latest_subject = eventdata['Subject'].iloc[0]
    latest_startdate = eventdata['Start Date'].iloc[0]
    latest_starttime = eventdata['Start Time'].iloc[0]
    # Lue websivusto pandasin dataframeen ja parsi sieltä html-taulukko, joka sisältää
    # ilmottautuneet pelaajat eventille
    player_amount_at_latest_event = pd.read_html(latest_event)
    players = player_amount_at_latest_event[0][4:5].iloc[0,1:2]
    # Muutetaan dataframen arvo stringiksi, jotta päästään siivomaan arvo
    players = players.to_string()
    # Poistetaan In teksti
    players = players.replace('In', '')
    # Poistetaan alusta rivinumero ja whitespacet
    players = players.replace(players[:2], '').strip()

    # Tehdään aikakäsittelyä
    d1 = arrow.get(latest_startdate, 'YYYY-MM-DD')
    date = d1.format('dddd')
    now = arrow.now()
    d2 = arrow.now()
    paiva = d2.format('dddd')
    today12pm = now.replace(hour=12, minute=1, second=0, microsecond=0)
    today9pm = now.replace(hour=21, minute=1, second=0, microsecond=0)

    if date == "Monday":
        fdate = 'Maanantai'
    elif date == "Tuesday":
        fdate = 'Tiistai'
    elif date == "Wednesday":
        fdate = 'Keskiviikko'
    elif date == "Thursday":
        fdate = 'Torstai'
    elif date == "Friday":
        fdate = 'Perjantai'
    elif date == "Saturday":
        fdate = 'Lauantai'
    elif date == "Sunday":
        fdate = 'Sunnuntai'
        
    # Lähetä Slackiin funktio
    def send_message_to_slack(text):
        from urllib import request, parse
        import json

        post = {"text": "{0}".format(text), "attachments": [
                                                    {
                                                        "author_name": "Nimenhuuto",
                                                        "author_icon": "https://slack-imgs.com/?c=1&o1=wi32.he32.si&url=https%3A%2F%2Fpaakonttori.nimenhuuto.com%2Ffavicon.ico",
                                                        "title": "Pääkonttori Nimenhuuto.com: Harkka, " + fdate[:2].casefold() + " " + d1.format('DD.MM.') + " klo " + latest_starttime,
                                                        "title_link": latest_event,
                                                        "text": "Pääkonttori: Harkka" + latest_subject.replace('Pääkonttori:', '') + " " + fdate[:2] + " klo " + d1.format('DD.MM.') + " " + latest_starttime + ". (Nimenhuuto.com, ilmoittautumisjärjestelmä joukkueille ja urheiluseuroille.)",
                                                        "thumb_url": "https://assets3.nimenhuuto.com/assets/logos/sports/floorball-3ca1ac6c8a35b7a0bcc3301874dc797d8be666c745eba72ad580810246deea56.png",
                                                    }
                                                ]
                                            }

        try:
            json_data = json.dumps(post)
            # ai -slack kanava
            #req = request.Request("https://hooks.slack.com/services/12345",
            # pääkonttorin_säbä -slack kanava
            req = request.Request("https://hooks.slack.com/services/12345",
                                data=json_data.encode('ascii'),
                                headers={'Content-Type': 'application/json'}) 
            resp = request.urlopen(req)
        except Exception as em:
            print("EXCEPTION: " + str(em))

    if int(players) == 0:
            send_message_to_slack("Mitä ihmettä? Ei yhtään pelaajia seuraavaan säbään? \nTäältä pääsee ilmoittautumaan jos linkki on hukassa.")
    else:
        if int(players) > 8:
                quote = [f"Vuoristoneuvosto Tuurakin olisi ylpeä! {players} on ilmoittautunut seuraavaan säbään", f"Ei tarvitse häpeillä yhtään tai huudella nimiä, koska {players} nimeä jo listalla säbään."]
                send_message_to_slack("<!here> " + random.choice(quote) + "\n\nMuistutuksena vielä kaikille että ilmottautumisdeadline on tiistaina klo 12:00. Jos vuorolle on deadlineen mennessä ilmoittautunut vähintään 8 pelaajaa, niin vuoro pidetään. Jos ilmoittautujia on 7 tai vähemmän, vuoro perutaan.\n\nTäältä pääsee ilmoittautumaan jos linkki on hukassa.")
        else:
                quote = [f"Näyttäisi että vain {players} on ilmoittautunut seuraavaan säbään. Saataisko jostain lisää porukkaa?", f"Jaahas vain {players} nimeä listalla. Saataisko jostain lisää porukkaa?", f"Johan on vähän nimiä listalla. Vaan {players}. Saataisko jostain lisää porukkaa?"]
                send_message_to_slack("<!here> " + random.choice(quote) + "\n\nMuistutuksena vielä kaikille että ilmottautumisdeadline on tiistaina klo 12:00. Jos vuorolle on deadlineen mennessä ilmoittautunut vähintään 8 pelaajaa, niin vuoro pidetään. Jos ilmoittautujia on 7 tai vähemmän, vuoro perutaan.\n\nTäältä pääsee ilmoittautumaan jos linkki on hukassa.")
