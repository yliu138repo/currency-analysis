from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class Notification:
    def __init__(self, not_config) -> None:
        print(not_config)
        self.__validate__(not_config)
        self.not_config = not_config
        
    def __validate__(self, not_config):
        if not_config.get("api_token") is None or not_config.get("channel") is None:
            raise Exception('Please provide all params for notifcation module')
        
    
    def send_msg(self, message):
        client = WebClient(token=self.not_config.get("api_token"))
        client.chat_postMessage(channel="#"+self.not_config.get("channel"), text=message)
    
    