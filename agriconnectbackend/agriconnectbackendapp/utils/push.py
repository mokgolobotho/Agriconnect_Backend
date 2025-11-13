# utils/push.py
from firebase_admin import messaging
from agriconnectbackendapp.models import UserDevice, Notification
from .firebase import init_firebase

class PushNotification:

    @staticmethod
    def send_push_notification(user_id: int, message: str, title: str = "AgriConnect Alert"):
        init_firebase()

        devices = UserDevice.objects.filter(user_id=user_id, active=True)
        if not devices.exists():
            print(f"⚠️ No active devices found for user {user_id}. Notification not sent.")
            return

        notif = Notification.objects.create(
            user_id=user_id,
            title=title,
            message=message
        )

        tokens = list(devices.values_list('fcm_token', flat=True))
        success_count = 0

        for token in tokens:
            try:
                message_payload = messaging.Message(
                    token=token,
                    notification=messaging.Notification(
                        title=title,
                        body=message
                    ),
                    data={
                        "notification_id": str(notif.id),
                        "type": "prediction_alert"
                    }
                )
                messaging.send(message_payload)
                success_count += 1
            except Exception as e:
                print(f"❌ Failed to send notification to token {token}: {e}")
                UserDevice.objects.filter(fcm_token=token).update(active=False)

        print(f"📣 Notification sent to {success_count}/{len(tokens)} devices for user {user_id}.")
