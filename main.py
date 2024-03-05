from notion_client import Client
import configparser
import scrapper as sc
from datetime import datetime
import pytz


config = configparser.ConfigParser()


config.read('config.ini')


token = config.get('Settings', 'token')
db_id = config.get('Settings', 'db')

notion = Client(auth=token)

response = notion.databases.retrieve(db_id)
title = response['title'][0]['text']['content']
print(f"Connection Success to", title)
events=sc.fetch_forex_factory_economic_calendar()

for event in events:
    date_object = datetime.strptime(event['datetime'], "%Y.%m.%d %H:%M")
    city_timezone = pytz.timezone('Europe/Kiev')
    localized_date_object = city_timezone.localize(date_object)
    iso_date_string = localized_date_object.strftime("%Y-%m-%dT%H:%M%z")
    response = notion.pages.create(
        parent={
            "type": "database_id",
            "database_id": db_id
        },
        properties={
            "Опис": { "type": "title",
                      "title": [{ "type": "text", "text": { "content": event['description'] } }]},
            "Дата та час": {
                "date": {
                    "start": iso_date_string
                }
            },
            "Валюта":{
                "rich_text":[
                    {
                        "type":"text",
                        "text":{
                            "content": event["currency"]
                        }
                    }
                ]
            },
            "Вплив":{
                "rich_text":[
                    {
                        "type":"text",
                        "text":{
                            "content": event["impact"]
                        }
                    }
                ]
            },
            "Фактичний":{
                "rich_text":[
                    {
                        "type":"text",
                        "text":{
                            "content": event["actual"]
                        }
                    }
                ]
            },
            "Прогноз":{
                "rich_text":[
                    {
                        "type":"text",
                        "text":{
                            "content": event["forecast"]
                        }
                    }
                ]
            },
            "Попередній":{
                "rich_text":[
                    {
                        "type":"text",
                        "text":{
                            "content": event["previous"]
                        }
                    }
                ]
            }
        }
    )

print("Parsed Succesfully")