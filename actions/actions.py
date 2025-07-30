import os
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import openai


class ActionOpenAIGenerate(Action):

    def name(self) -> Text:
        return "action_openai_generate"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Получаем последнее сообщение пользователя
        user_message = tracker.latest_message.get("text")

        # Ключ уже в окружении
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Вызываем ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7,
        )

        # Берём ответ
        answer = response.choices[0].message["content"].strip()

        # Отправляем его пользователю
        dispatcher.utter_message(text=answer)

        return []