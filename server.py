from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List
import uuid
from datetime import datetime, timezone
from email_service import send_booking_email


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class BookingRequest(BaseModel):
    pickupLocation: str
    pickupAddress: str
    dropOffLocation: str
    dropOffAddress: str
    preferredPickupDate: str
    deliveryType: str
    numberOfBags: int
    fullName: str
    email: EmailStr
    phone: str

class Booking(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pickupLocation: str
    pickupAddress: str
    dropOffLocation: str
    dropOffAddress: str
    preferredPickupDate: str
    deliveryType: str
    numberOfBags: int
    fullName: str
    email: str
    phone: str
    status: str = "pending"
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FranchiseInquiryRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    city: str
    franchiseType: str

class FranchiseInquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: str
    city: str
    franchiseType: str
    status: str = "new"
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

@api_router.post("/booking", response_model=Booking)
async def create_booking(booking_request: BookingRequest):
    """
    Create a new booking request and send email notification
    """
    try:
        # Create booking object
        booking_data = booking_request.model_dump()
        booking = Booking(**booking_data)
        
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = booking.model_dump()
        doc['createdAt'] = doc['createdAt'].isoformat()
        
        # Save to database
        await db.bookings.insert_one(doc)
        logger.info(f"Booking created: {booking.id} for {booking.fullName}")
        
        # Send email notification
        email_sent = send_booking_email(booking.model_dump())
        
        if not email_sent:
            logger.warning(f"Email notification failed for booking {booking.id}")
        
        return booking
        
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create booking")

@api_router.get("/bookings", response_model=List[Booking])
async def get_bookings():
    """
    Get all bookings (for admin purposes)
    """
    # Exclude MongoDB's _id field from the query results
    bookings = await db.bookings.find({}, {"_id": 0}).sort("createdAt", -1).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for booking in bookings:
        if isinstance(booking['createdAt'], str):
            booking['createdAt'] = datetime.fromisoformat(booking['createdAt'])
    
    return bookings

@api_router.post("/franchise-inquiry", response_model=FranchiseInquiry)
async def create_franchise_inquiry(inquiry_request: FranchiseInquiryRequest):
    """
    Create a new franchise inquiry and send email notification to info@bagdrop.co
    """
    try:
        # Create inquiry object
        inquiry_data = inquiry_request.model_dump()
        inquiry = FranchiseInquiry(**inquiry_data)
        
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = inquiry.model_dump()
        doc['createdAt'] = doc['createdAt'].isoformat()
        
        # Save to database
        await db.franchise_inquiries.insert_one(doc)
        logger.info(f"Franchise inquiry created: {inquiry.id} for {inquiry.name}")
        
        # Send email notification to info@bagdrop.co
        from email_service import send_franchise_inquiry_email
        email_sent = send_franchise_inquiry_email(inquiry.model_dump())
        
        if not email_sent:
            logger.warning(f"Email notification failed for franchise inquiry {inquiry.id}")
        
        return inquiry
        
    except Exception as e:
        logger.error(f"Error creating franchise inquiry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create franchise inquiry")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
