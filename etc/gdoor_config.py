# List and configure all garage doors
SENSORS = [
    {
        'pin': 15,              # GPIO pin to which the sensor is connected
        'name': "GARAGE Door",  # Sensor name
        'alert_notify': 'Y',    # Flag to indicate alert notification
        'alert_notification_interval_minutes': 0.34   # Time interval for notification
    },

     {
         'pin': 40,
         'name': "Front Entry Door",
         'alert_notify': 'N',
        'alert_notification_interval_minutes': 0.25
     }
]
