from firebase_admin import messaging

from notifications.types import SendType


def send(tokens, notification=None, data=None, **kwargs):
    message = messaging.MulticastMessage(
        notification=notification, data=data, tokens=tokens, **kwargs
    )
    response = messaging.send_multicast(message)
    print("{0} messages were sent successfully".format(response.success_count))
    return response


def send_to_topic(topic, notification=None, data=None, **kwargs):
    message = messaging.Message(
        notification=notification, data=data, topic=topic, **kwargs
    )
    response = messaging.send(message)
    print("Successfully sent message:", response)
    return response


def send_notification(
    title=None,
    body=None,
    image=None,
    link=None,
    data=None,
    target=SendType.ADMIN,
    tokens=None,
):
    if target == SendType.ADMIN:
        return send_to_topic(
            topic="admin",
            notification=messaging.Notification(title=title, body=body, image=image),
            android=messaging.AndroidConfig(data=data, priority="high"),
        )
    elif target == SendType.CUSTOMERS:
        return send_to_topic(
            topic="customer",
            notification=messaging.Notification(title=title, body=body, image=image),
            android=messaging.AndroidConfig(data=data, priority="high"),
        )
    elif target == SendType.CUSTOMER and tokens:
        return send(
            tokens=list(tokens) or [],
            notification=messaging.Notification(title=title, body=body, image=image),
            android=messaging.AndroidConfig(data=data, priority="high"),
        )
