import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_booking_email(booking_data):

    try:

        html = f"""
        <html>
        <body style="font-family:Arial,sans-serif; line-height:1.6;">

            <h2 style="color:#ea580c;">
                🎒 New BagDrop Booking Inquiry
            </h2>

            <hr>

            <h3>Customer Details</h3>

            <p><strong>Name:</strong> {booking_data.get('fullName')}</p>
            <p><strong>Phone:</strong> {booking_data.get('phone')}</p>
            <p><strong>Email:</strong> {booking_data.get('email')}</p>

            <hr>

            <h3>Pickup Details</h3>

            <p><strong>Pickup Location:</strong> {booking_data.get('pickupLocation')}</p>
            <p><strong>Pickup Address:</strong> {booking_data.get('pickupAddress')}</p>

            <hr>

            <h3>Drop Details</h3>

            <p><strong>Drop Location:</strong> {booking_data.get('dropOffLocation')}</p>
            <p><strong>Drop Address:</strong> {booking_data.get('dropOffAddress')}</p>

            <hr>

            <h3>Baggage Details</h3>

            <p><strong>Number of Bags:</strong> {booking_data.get('numberOfBags')}</p>

            <hr>

            <h3>Schedule</h3>

            <p><strong>Preferred Pickup Date:</strong> {booking_data.get('preferredPickupDate')}</p>
            <p><strong>Preferred Delivery Date:</strong> {booking_data.get('deliveryDate')}</p>

        </body>
        </html>
        """

        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "BagDrop <booking@bagdrop.co>",
                "to": ["info@bagdrop.co"],
                "subject": f"New Booking Inquiry - {booking_data.get('fullName')}",
                "html": html
            }
        )

        if response.status_code in [200, 201]:
            print("Booking email sent successfully")
            return True

        print("Resend Error:", response.text)
        return False

    except Exception as e:
        print("Error sending booking email:", str(e))
        return False

