import json
import traceback

from mastodon import Mastodon
import os
import base64
from ai_battler.chat.models import ChatModel
from urllib.parse import urlparse

from .chatbot import ChatBot
from .utils import remove_html_tags
from ..ai.arena import Arena
from boto3 import client as boto3_client


def get_notification(mastodon, notification_id):
    notification = mastodon.notifications(id=notification_id)
    user_id = notification["account"]["acct"]
    if "@" not in user_id:
        user_id = f'{user_id}@{urlparse(os.getenv("MASTODON_SERVER")).hostname}'

    print(notification["status"]["content"])
    return {
        "user_id": user_id,
        "acct": notification["account"]["acct"],
        "status_id": notification["status"]["id"],
        "visibility": notification["status"]["visibility"],
        "content": remove_html_tags(notification["status"]["content"]),
    }


def process_mention(mastodon, notification_id, force_process=False):
    if not ChatModel.lock(str(notification_id)) and not force_process:
        print("Already processed: notificationId={}".format(notification_id))
        return

    lambda_client = boto3_client(
        "lambda",
        region_name=os.getenv("REGION"),
    )
    lambda_client.invoke(
        FunctionName=os.getenv("WORKER_FUNCTION"),
        InvocationType="Event",
        Payload=json.dumps({"notification_id": notification_id}),
    )


def process_worker(notification_id):
    mastodon = Mastodon(
        access_token=os.getenv("ACCESS_TOKEN"),
        api_base_url=os.getenv("MASTODON_SERVER"),
    )

    info = get_notification(mastodon, notification_id)
    try:
        visibility = info["visibility"]
        if visibility == "direct" and info["acct"] != "osa9":
            return

        bot = ChatBot(Arena(api_key=os.getenv("OPENAI_API_KEY")))
        res = bot.action(info["user_id"], info["content"])
        if res is not None:
            mastodon.status_post(
                "@" + info["acct"] + " " + res,
                in_reply_to_id=info["status_id"],
                visibility=visibility,
            )
    except Exception as ex:
        mastodon.status_post(
            "@" + info["acct"] + " エラー" + str(ex)[:256],
            in_reply_to_id=info["status_id"],
            visibility=info["visibility"],
        )
        print("Unknown error")
        print(ex)
        print(traceback.format_exc())


def handle_push_notification(body, encryption, crypto_key):
    mastodon = Mastodon(
        access_token=os.getenv("ACCESS_TOKEN"),
        api_base_url=os.getenv("MASTODON_SERVER"),
    )

    try:
        priv_key = json.load(open("keys/privkey"))
        priv_key["auth"] = base64.b64decode(priv_key["auth"])
        notification = mastodon.push_subscription_decrypt_push(
            body, priv_key, encryption, crypto_key
        )
        if notification["notification_type"] == "mention":
            process_mention(mastodon, notification["notification_id"])
        if notification["notification_type"] == "follow":
            pass
    except Exception as ex:
        print("Unknown error")
        print(ex)
        print(traceback.format_exc())
        mastodon.status_post("@osa9 " + str(ex), visibility="direct")
        raise ex

    return True
