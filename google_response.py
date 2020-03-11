import os

from dotenv import load_dotenv
import dialogflow_v2 as dialogflow

PROJECT_ID = os.getenv('PROJECT_ID')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def detect_intent_texts(session_id, text, language_code='ru', project_id=PROJECT_ID):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    if response.query_result.intent.is_fallback:
        return None
    answer = response.query_result.fulfillment_text
    return answer
