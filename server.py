from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from email_service import send_booking_email

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bagdrop-website.vercel.app",
        "https://www.bagdrop.co",
        "https://bagdrop.co"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)



class BookingRequest(BaseModel):
    pickupLocation: str
    pickupAddress: str

    dropOffLocation: str
    dropOffAddress: str

    numberOfBags: int

    preferredPickupDate: str
    deliveryDate: str

    fullName: str
    phone: str
    email: EmailStr


@app.get("/")
async def root():
    return {
        "message": "BagDrop Website Backend Running"
    }


@app.post("/api/booking-inquiry")
async def booking_inquiry(data: BookingRequest):

    try:

        email_sent = send_booking_email(data.model_dump())

        if not email_sent:
            raise HTTPException(
                status_code=500,
                detail="Failed to send booking inquiry email"
            )

        return {
            "success": True,
            "message": "Booking inquiry submitted successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

