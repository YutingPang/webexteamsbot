def issue_card():
    c = """
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
    return c
