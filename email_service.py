import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_booking_email(booking_data):
    """
    Send Booking Inquiry Email using Resend
    """

    try:

        html = f"""
        <html>
        <body style="font-family:Arial,sans-serif">

            <h2 style="color:#ea580c;">
                🎒 New BagDrop Booking Inquiry
            </h2>

            <hr>

            <h3>Customer Details</h3>

            <p><strong>Name:</strong> {booking_data.get('name')}</p>
            <p><strong>Phone:</strong> {booking_data.get('phone')}</p>
            <p><strong>Email:</strong> {booking_data.get('email')}</p>

            <hr>

            <h3>Travel Details</h3>

            <p><strong>Airport:</strong> {booking_data.get('airport')}</p>
            <p><strong>Flight Number:</strong> {booking_data.get('flightNumber')}</p>

            <hr>

            <h3>Pickup & Delivery</h3>

            <p><strong>Pickup Location:</strong> {booking_data.get('pickupLocation')}</p>
            <p><strong>Drop Location:</strong> {booking_data.get('dropLocation')}</p>

            <hr>

            <h3>Baggage Details</h3>

            <p><strong>Number of Bags:</strong> {booking_data.get('bags')}</p>

            <hr>

            <h3>Additional Message</h3>

            <p>{booking_data.get('message')}</p>

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
                "subject": f"New Booking Inquiry - {booking_data.get('name')}",
                "html": html
            }
        )

        if response.status_code in [200, 201]:
            print("✅ Booking email sent successfully")
            return True

        print("❌ Resend Error:", response.text)
        return False

    except Exception as e:
        print("❌ Error sending booking email:", str(e))
        return False
