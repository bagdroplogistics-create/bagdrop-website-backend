import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_booking_email(booking_data):

    try:

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>BagDrop Booking Inquiry</title>
        </head>
        
        <body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,sans-serif;">
        
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px 0;">
        <tr>
        <td align="center">
        
        <table width="650" cellpadding="0" cellspacing="0"
        style="
        background:#ffffff;
        border-radius:10px;
        overflow:hidden;
        box-shadow:0 2px 10px rgba(0,0,0,0.08);
        ">
        
        <tr>
        <td
        style="
        background:#ff6b35;
        padding:35px;
        text-align:center;
        color:#ffffff;
        "
        >
        <h1 style="margin:0;font-size:34px;font-weight:bold;">
        BAGDROP
        </h1>
        
        <p style="margin-top:10px;font-size:14px;">
        BAG. BOX. DELIVERED.
        </p>
        </td>
        </tr>
        
        <tr>
        <td style="padding:30px;">
        
        <h2
        style="
        color:#ff6b35;
        margin-top:0;
        margin-bottom:15px;
        "
        >
        🧳 New Booking Inquiry Received
        </h2>
        
        <div
        style="
        background:#fff7f3;
        border:1px solid #ffd5c4;
        padding:15px;
        border-radius:8px;
        margin-bottom:25px;
        "
        >
        A new booking inquiry has been submitted through the BagDrop website.
        </div>
        
        <h3 style="color:#ff6b35;">
        Customer Details
        </h3>
        
        <table width="100%" cellpadding="8" cellspacing="0"
        style="background:#fafafa;border-radius:8px;">
        <tr>
        <td width="35%"><strong>Name</strong></td>
        <td>{booking_data.get('fullName')}</td>
        </tr>
        
        <tr>
        <td><strong>Phone</strong></td>
        <td>{booking_data.get('phone')}</td>
        </tr>
        
        <tr>
        <td><strong>Email</strong></td>
        <td>{booking_data.get('email')}</td>
        </tr>
        </table>
        
        <br>
        
        <h3 style="color:#ff6b35;">
        Pickup Details
        </h3>
        
        <table width="100%" cellpadding="8" cellspacing="0"
        style="background:#fafafa;border-radius:8px;">
        <tr>
        <td width="35%"><strong>Pickup Location</strong></td>
        <td>{booking_data.get('pickupLocation')}</td>
        </tr>
        
        <tr>
        <td><strong>Pickup Address</strong></td>
        <td>{booking_data.get('pickupAddress')}</td>
        </tr>
        </table>
        
        <br>
        
        <h3 style="color:#ff6b35;">
        Drop Details
        </h3>
        
        <table width="100%" cellpadding="8" cellspacing="0"
        style="background:#fafafa;border-radius:8px;">
        <tr>
        <td width="35%"><strong>Drop Location</strong></td>
        <td>{booking_data.get('dropOffLocation')}</td>
        </tr>
        
        <tr>
        <td><strong>Drop Address</strong></td>
        <td>{booking_data.get('dropOffAddress')}</td>
        </tr>
        </table>
        
        <br>
        
        <h3 style="color:#ff6b35;">
        Schedule
        </h3>
        
        <table width="100%" cellpadding="8" cellspacing="0"
        style="background:#fafafa;border-radius:8px;">
        <tr>
        <td width="35%"><strong>Pickup Date</strong></td>
        <td>{booking_data.get('preferredPickupDate')}</td>
        </tr>
        
        <tr>
        <td><strong>Delivery Date</strong></td>
        <td>{booking_data.get('deliveryDate')}</td>
        </tr>
        </table>
        
        <br>
        
        <h3 style="color:#ff6b35;">
        Baggage Information
        </h3>
        
        <table width="100%" cellpadding="8" cellspacing="0"
        style="background:#fafafa;border-radius:8px;">
        <tr>
        <td width="35%"><strong>Number Of Bags</strong></td>
        <td>{booking_data.get('numberOfBags')}</td>
        </tr>
        </table>
        
        <div
        style="
        margin-top:30px;
        padding-top:20px;
        border-top:1px solid #e5e5e5;
        font-size:13px;
        color:#666666;
        text-align:center;
        "
        >
        This inquiry was submitted from the BagDrop website.
        <br><br>
        © BagDrop Logistics Solutions Pvt. Ltd.
        </div>
        
        </td>
        </tr>
        
        </table>
        
        </td>
        </tr>
        </table>
        
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
               "subject": f"🧳 New Booking Inquiry - {booking_data.get('fullName')}",
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

