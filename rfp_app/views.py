from django.shortcuts import render, redirect
from .models import RFP
import re
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()
import requests

# Create your views here.
def index(request):
    return render(request,"index.html")

def scrape_1(request):
    import requests
    from bs4 import BeautifulSoup

    # URL of the website to scrape
    url = 'https://marketplace.dailyherald.com/il/bid-notices/search?limit=240'

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Save the HTML code to a file
    div_element = soup.find('div', id='ap_waterfall_container')

    # Extract and print data from elements inside the div
    for div in div_element.find_all('div', class_='list-panel'):
        inner_div = div.find('div',class_="list-panel-info")
        posted_on = inner_div.find('div', class_="post-summary-date").text
        numbers = re.findall(r'\d+', posted_on)
        current_date = datetime.now().date()
        numbers = numbers[0]
        new_date = current_date - timedelta(days=int(numbers))
        title_inner_div = inner_div.find('div', class_="post-summary-title")
        title = title_inner_div.find('p', class_="desktop").text
        desc = inner_div.find('p', class_="post-copy desktop").text
        if RFP.objects.filter(title=title).exists():
            continue
        RFP.objects.create(posted_date=new_date, title=title, description=desc)

def scrape_2(request):
    import requests
    from bs4 import BeautifulSoup

    # URL of the website to scrape
    url = 'https://cookcountyil.bonfirehub.com/portal/?tab=openOpportunities'

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Save the HTML code to a file
    with(open('cookcounty.html', 'w', encoding='utf-8')) as file:
        file.write(str(soup))

    table = soup.find('table')
    tbody = table.find('tbody')
    even_rows = tbody.find_all('tr', class_='even')
    for x in even_rows:
        td = x.find_all('td')
        print(td)
        title = td[2].find('strong').text
        desc = td[3].text
        rfx_bid_number = td[1].text
        duedate= td[4].text
        print(title, desc, rfx_bid_number, duedate)

def scrape_3(request):
    import requests
    from bs4 import BeautifulSoup

    # URL of the website to scrape
    url = 'https://apps.ccc.edu/bid/View.aspx'

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table',id="ctl00_ContentPlaceHolder1_Bid_info")
    rows = table.find_all('tr')
    for x in rows:
        try:
            if x.find('th'):
                continue
            td = x.find_all('td')
            title = td[1].text
            posted_date = td[3].text
            rfx_bid_number = td[0].text
            duedate= td[2].text
            
            if duedate == "None":
                duedate = "N/A"
            else:
                due_date_object = datetime.strptime(duedate, "%B %d, %Y")
                due_posted_date = datetime.strftime(due_date_object, "%Y-%m-%d")

            posted_date_object = datetime.strptime(posted_date, "%B %d, %Y")
            formatted_posted_date = datetime.strftime(posted_date_object, "%Y-%m-%d")

            if RFP.objects.filter(title=title).exists():
                continue
            RFP.objects.create(posted_date=formatted_posted_date, title=title, rfx_bid_number=rfx_bid_number, due_date=due_posted_date)

        except Exception as e:
            print(e)
            continue

def scrape(request):
    website = request.GET["website"]
    try:
        if int(website) == 1:
            scrape_1(request)
        if int(website) == 2:
            scrape_2(request)
        if int(website) == 3:
            scrape_3(request)
        return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')
    
def send_adaptive_cards(request):
    unsenent_rfp = RFP.objects.filter(sent_to_ms_teams=False)
    for x in unsenent_rfp:
        adaptive_card = """ 
        {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": null,
                    "content":{
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.4",
                        "body": [
                            {
                                "type": "Container",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": \""""+str(x.title)+"""\",
                                        "weight": "Bolder",
                                        "size": "Medium"
                                    }
                                ]
                            },
                            {
                                "type": "Container",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": \""""+str(x.description)+"""\",
                                        "wrap": true
                                    },
                                    {
                                        "type": "FactSet",
                                        "facts": [
                                            {
                                                "title": "Posting Entity:",
                                                "value": \""""+str(x.buyer_agent_name)+"""\"
                                            },
                                            {
                                                "title": "Due Date:",
                                                "value": \""""+str(x.due_date)+"""\"
                                            },
                                            {
                                                "title": "Bid type:",
                                                "value":  \""""+str(x.rfx_type)+"""\"
                                            },
                                            {
                                                "title": "Created date:",
                                                "value": \""""+str(x.posted_date)+"""\"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "actions": [
                            {
                                "type": "Action.ShowCard",
                                "title": "Schedule Bidders Conference",
                                "card": {
                                    "type": "AdaptiveCard",
                                    "body": [
                                        {
                                            "type": "Input.Text",
                                            "id": "comment",
                                            "isMultiline": true,
                                            "placeholder": "Enter your comment"
                                        }
                                    ],
                                    "actions": [
                                        {
                                            "type": "Action.Submit",
                                            "title": "Schedule Bidders Conference",
                                            "data": {
                                                "action": "scheduleConference"
                                            }
                                        },
                                        {
                                            "type": "Action.Submit",
                                            "title": "Ask More Questions"
                                        }
                    
                                    ]
                                }
                            },
                            {
                                "type": "Action.OpenUrl",
                                "title": "Open in web browser",
                                "url": "https://adaptivecards.io"
                            },
                            {
                                "type": "Action.OpenUrl",
                                "title": "Not Interested",
                                "url": "https://adaptivecards.io"
                            }
                        ]
                    }
                }
            ]
        }

        """

        webhookUrl = os.environ.get('MS_TEAMS_WEBHOOK')
        client = requests.Session()

        client.headers['Accept'] = 'application/json'
        headers = {
            'Content-Type': 'application/json'
        }
        payload = adaptive_card.encode('utf-8')

        # Send the POST request
        response = client.post(webhookUrl, data=payload, headers=headers)
    
        # Check the response status
        if response.status_code == 200:
            print("Card sent successfully")
            x.sent_to_ms_teams = True
            x.save()
        else:
            print("Failed to send the card. Status code:", response.status_code)
            print(response.text)

    # here now we have to send these cards to the ms teams
    return redirect('home')




