import json
import traceback
import base64

from ai_battler.chat.mastodon_api import handle_push_notification, process_worker


def push_notification(event, _context):
    try:
        handle_push_notification(
            base64.b64decode(event["body"]),
            event["headers"].get("encryption"),
            event["headers"].get("crypto-key"),
        )
        response = {"statusCode": 200, "body": json.dumps({"ok": True})}
        return response
    except Exception as ex:
        print("Unknown error")
        print(ex)
        print(traceback.format_exc())
        response = {"statusCode": 200, "body": json.dumps({"ok": False})}
        return response


def worker(event, _context):
    print(event)
    process_worker(event["notification_id"])


def test(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"event": "test"}),
    }
