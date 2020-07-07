# -*- coding: utf-8 -*-
"""
Sample code for using webexteamsbot
"""

import os
import requests
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
import sys
import json

# Retrieve required details from environment variables
bot_email = os.getenv("TEAMS_BOT_EMAIL")
teams_token = os.getenv("TEAMS_BOT_TOKEN")
bot_url = os.getenv("TEAMS_BOT_URL")
bot_app_name = os.getenv("TEAMS_BOT_APP_NAME")

# Example: How to limit the approved Webex Teams accounts for interaction
#          Also uncomment the parameter in the instantiation of the new bot
# List of email accounts of approved users to talk with the bot
# approved_users = [
#     "josmith@demo.local",
# ]

# If any of the bot environment variables are missing, terminate the app
if not bot_email or not teams_token or not bot_url or not bot_app_name:
    print(
        "sample.py - Missing Environment Variable. Please see the 'Usage'"
        " section in the README."
    )
    if not bot_email:
        print("TEAMS_BOT_EMAIL")
    if not teams_token:
        print("TEAMS_BOT_TOKEN")
    if not bot_url:
        print("TEAMS_BOT_URL")
    if not bot_app_name:
        print("TEAMS_BOT_APP_NAME")
    sys.exit()

# Create a Bot Object
#   Note: debug mode prints out more details about processing to terminal
#   Note: the `approved_users=approved_users` line commented out and shown as reference
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    # approved_users=approved_users,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},
    ],
)


# Create a custom bot greeting function returned when no command is given.
# The default behavior of the bot is to return the '/help' command response
def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, I'm dCloud Support bot. ".format(sender.firstName)
    response.markdown += "Enter **/support** to start chatting with our support Engineer. "
    response.markdown += "Or see what I can do by asking for **/help**."
    return response


# Create functions that will be linked to bot commands to add capabilities
# ------------------------------------------------------------------------

# A simple command that returns a basic string that will be sent as a reply
def do_something(incoming_msg):
    """
    Sample function to do some action.
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    return "i did what you said - {}".format(incoming_msg.text)


# This function generates a basic adaptive card and sends it to the user
# You can use Microsofts Adaptive Card designer here:
# https://adaptivecards.io/designer/. The formatting that Webex Teams
# uses isn't the same, but this still helps with the overall layout
# make sure to take the data that comes out of the MS card designer and
# put it inside of the "content" below, otherwise Webex won't understand
# what you send it.
def show_card(incoming_msg):
    attachment = """
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.1",
                "body": [
                    {
                        "type": "ColumnSet",
                        "columns": [
                            {
                                "type": "Column",
                                "items": [
                                    {
                                        "type": "Image",
                                        "style": "Person",
                                        "url": "https://developer.webex.com/images/webex-teams-logo.png",
                                        "size": "Medium",
                                        "height": "50px"
                                    }
                                ],
                                "width": "auto"
                            },
                            {
                                "type": "Column",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "Cisco dCloud Support",
                                        "weight": "Lighter",
                                        "color": "Accent"
                                    },
                                    {
                                        "type": "TextBlock",
                                        "weight": "Bolder",
                                        "text": "Issue Collection Form",
                                        "horizontalAlignment": "Left",
                                        "wrap": true,
                                        "color": "Light",
                                        "size": "Large",
                                        "spacing": "Small"
                                    }
                                ],
                                "width": "stretch"
                            }
                        ]
                    },
                    {
                        "type": "TextBlock",
                        "text": "Issue Summary:",
                        "wrap": true
                    },
                    {
                        "type": "Input.Text",
                        "placeholder": "Text Field",
                        "style": "text",
                        "maxLength": 0,
                        "id": "summary"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Data Center:",
                        "wrap": true
                    },
                    {
                        "type": "Input.ChoiceSet",
                        "id": "datacenter",
                        "value": "Red",
                        "choices": [
                            {
                                "title": "RTP",
                                "value": "RTP"
                            },
                            {
                                "title": "SJC",
                                "value": "SJC"
                            },
                            {
                                "title": "EMEAR",
                                "value": "EMEAR"
                            },
                            {
                                "title": "SNG",
                                "value": "SNG"
                            },
                            {
                                "title": "CHI",
                                "value": "CHI"
                            }
                        ]
                    },
                    {
                        "type": "TextBlock",
                        "text": "Demo Name:",
                        "wrap": true
                    },
                    {
                        "type": "Input.Text",
                        "placeholder": "Text Field",
                        "style": "text",
                        "maxLength": 0,
                        "id": "demo_name"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Session ID:",
                        "wrap": true
                    },
                    {
                        "type": "Input.ChoiceSet",
                        "id": "Session_id",
                        "value": "Red",
                        "choices": [
                            {
                                "title": "1598",
                                "value": "1598"
                            },
                            {
                                "title": "1599",
                                "value": "1599"
                            }
                        ]
                    },
                    {
                        "type": "Input.Toggle",
                        "title": "Create a support ticket?",
                        "id": "create_ticket",
                        "wrap": true,
                        "value": "true"
                    },
                    {
                        "type": "Input.Toggle",
                        "title": "Start Chat with Support Engineer?",
                        "id": "start_chat",
                        "wrap": true,
                        "value": "true"
                    }
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                        "data": {
                            "form_action": "Submit"
                        }
                    }
                ]
            }
        }
    """
    backupmessage = "This is an example using Adaptive Cards."

    c = create_message_with_attachment(
        incoming_msg.roomId, msgtxt=backupmessage, attachment=json.loads(attachment)
    )
    print(c)
    return ""


# An example of how to process card actions
def handle_cards(api, incoming_msg):
    """
    Sample function to handle card actions.
    :param api: webexteamssdk object
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    # Loopkup details about sender
    # sender = bot.teams.people.get(incoming_msg.personId)
    # print(sender)
    m = get_attachment_actions(incoming_msg["data"]["id"])
    sender = m['personId']
    res_create_ticket = None
    if m["inputs"]["create_ticket"]:
        res_create_ticket = create_jira_issue(m)

    if m["inputs"]["start_chat"]:
        res = create_room(res_create_ticket['key'])
        print(res)
        rid = res['id']
        add_people_to_room(rid, sender)
        add_people_to_room(rid, 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jNjQxYmEzYy1lYWY4LTQ3OGUtYTRiNC03MjNkYjUyYjc4OGU')

    # response = Response()

    msg = "[{0}](http://lon-xse-services.cisco.com/browse/{0}) created, " \
        "Please join Webex space **{0}** to " \
        "chat with support engineer,".format(res_create_ticket['key'])

    return msg


def create_jira_issue(data):
    headers = {
        "content-type": "application/json",
        "Authorization": "Basic eXV0cGFuZy1sb2NhbDp6YXExeHN3Mg=="
    }

    url = "http://lon-xse-services.cisco.com/rest/api/2/issue"

    if len(data['inputs']['summary']) <= 1:
        data['inputs']['summary'] = 'TEST Summary'

    data = {
        "fields": {
            "project": {
                "key": "TKT"
            },
            "summary": data['inputs']['summary'],
            "description": "test jira res",
            "issuetype": {
                "name": "dCloud Support"
            }
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()


def add_people_to_room(rid, people):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://webexapis.com/v1/memberships"
    data = {"roomId": rid, "personId": people}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def create_room(rname):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://webexapis.com/v1/rooms"
    data = {"title": rname}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


# Temporary function to send a message with a card attachment (not yet
# supported by webexteamssdk, but there are open PRs to add this
# functionality)
def create_message_with_attachment(rid, msgtxt, attachment):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://api.ciscospark.com/v1/messages"
    data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


# Temporary function to get card attachment actions (not yet supported
# by webexteamssdk, but there are open PRs to add this functionality)
def get_attachment_actions(attachmentid):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://api.ciscospark.com/v1/attachment/actions/" + attachmentid
    response = requests.get(url, headers=headers)
    return response.json()


# An example using a Response object.  Response objects allow more complex
# replies including sending files, html, markdown, or text. Rsponse objects
# can also set a roomId to send response to a different room from where
# incoming message was recieved.
def ret_message(incoming_msg):
    """
    Sample function that uses a Response object for more options.
    :param incoming_msg: The incoming message object from Teams
    :return: A Response object based reply
    """
    # Create a object to create a reply.
    response = Response()

    # Set the text of the reply.
    response.text = "Here's a fun little meme."

    # Craft a URL for a file to attach to message
    u = "https://sayingimages.com/wp-content/uploads/"
    u = u + "aaaaaalll-righty-then-alrighty-meme.jpg"
    response.files = u
    return response


# An example command the illustrates using details from incoming message within
# the command processing.
def current_time(incoming_msg):
    """
    Sample function that returns the current time for a provided timezone
    :param incoming_msg: The incoming message object from Teams
    :return: A Response object based reply
    """
    # Extract the message content, without the command "/time"
    timezone = bot.extract_message("/time", incoming_msg.text).strip()

    # Craft REST API URL to retrieve current time
    #   Using API from http://worldclockapi.com
    u = "http://worldclockapi.com/api/json/{timezone}/now".format(timezone=timezone)
    r = requests.get(u).json()

    # If an invalid timezone is provided, the serviceResponse will include
    # error message
    if r["serviceResponse"]:
        return "Error: " + r["serviceResponse"]

    # Format of returned data is "YYYY-MM-DDTHH:MM<OFFSET>"
    #   Example "2018-11-11T22:09-05:00"
    returned_data = r["currentDateTime"].split("T")
    cur_date = returned_data[0]
    cur_time = returned_data[1][:5]
    timezone_name = r["timeZoneName"]

    # Craft a reply string.
    reply = "In {TZ} it is currently {TIME} on {DATE}.".format(
        TZ=timezone_name, TIME=cur_time, DATE=cur_date
    )
    return reply


def sign_in(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, You are on call shift now. ".format(sender.firstName)
    response.markdown += "New chat case will be signed to you!"
    return response


def sign_out(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, You are off now. ".format(sender.firstName)
    response.markdown += "Have a good day!"
    return response


def survey(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, this function still in development ".format(sender.firstName)
    response.markdown += "Thank you for your feedback!"
    return response


# Create help message for current_time command
current_time_help = "Look up the current time for a given timezone. "
current_time_help += "_Example: **/time EST**_"

# Set the bot greeting.
bot.set_greeting(greeting)

# Add new commands to the bot.
bot.add_command("/survey", "Please give us feedback.", survey)
bot.add_command("/sign-in", "This is **SE only** function, SE on call sign-in", sign_in)
bot.add_command("/sign-out", "This is **SE only** function, SE on call sign-out", sign_out)
bot.add_command("attachmentActions", "*", handle_cards)
bot.add_command("/support", "start live chat with Support Engineer", show_card)
# bot.add_command("/dosomething", "help for do something", do_something)
# bot.add_command(
#     "/demo", "Sample that creates a Teams message to be returned.", ret_message
# )
# bot.add_command("/time", current_time_help, current_time)

# Every bot includes a default "/echo" command.  You can remove it, or any
# other command with the remove_command(command) method.
bot.remove_command("/echo")

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)
