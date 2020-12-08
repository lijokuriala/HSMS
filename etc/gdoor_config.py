# List and configure all garage doors
SENSORS = [
    {
        'pin': 15,
        'name': "GARAGE Door",
        'alert_notify': 'Y',
        'alert_notification_interval_minutes': 0.3
    },

     {
         'pin': 40,
         'name': "Front Entry Door",
         'alert_notify': 'N',
        'alert_notification_interval_minutes': 0.25
     }
]
