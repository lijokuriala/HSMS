# List and configure all garage doors
SENSORS = [
    {
        'pin': 15,
        'name': "Main Garage Door",
        'alert_notify': 'Y',
        'alert_notification_interval_minutes': 0.25
    },

     {
         'pin': 40,
         'name': "Test Garage Door",
         'alert_notify': 'N',
        'alert_notification_interval_minutes': 0.5
     }
]
