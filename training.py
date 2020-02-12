import dialogflow_v2 as dialogflow
from google.protobuf.json_format import MessageToDict
import json
import os
import argparse

PROJECT_ID = os.getenv('PROJECT_ID')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def create_intent(name, training_phrases, messages, parameters=None, project_id=PROJECT_ID):
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)
    intent = {
        'display_name': name,
        'training_phrases': training_phrases,
        'parameters': parameters,
        'messages': messages,
    }
    intent = intents_client.create_intent(
        parent, intent, intent_view=dialogflow.enums.IntentView.INTENT_VIEW_FULL)

    return MessageToDict(intent, preserving_proto_field_name=True)


def main():
    parser = argparse.ArgumentParser(
        description='Программа добавляет intent в ваш проект на dialogflow из файла json'
    )
    parser.add_argument('file', help='input json file')
    args = parser.parse_args()

    with open(args.file) as json_file:
        raw_data = json.load(json_file, encoding='utf-8')

    for intent in raw_data.items():
        name = intent[0]
        phrases = intent[1]['questions']
        training_phrases = [{'type': 'EXAMPLE', 'parts': [
            {'text': phrase}]} for phrase in phrases]
        bot_answers = [intent[1]['answer']]
        messages = [{'text': {'text': [answer]}} for answer in bot_answers]

        create_intent(name, training_phrases, messages,
                      parameters=None, project_id=PROJECT_ID)


if __name__ == "__main__":
    main()
