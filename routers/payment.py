from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Payment, Course, User
from database import get_db
from services.auth import get_current_user
import stripe
import os
from dotenv import load_dotenv
from stripe.error import CardError, RateLimitError, InvalidRequestError, AuthenticationError, APIConnectionError, StripeError


# Load environment variables from .env file
load_dotenv()

# Set up Stripe API keys
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # Use environment variable for security
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")

router = APIRouter()

@router.post("/create-payment-intent/")
def create_payment_intent(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Retrieve course
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course or not course.is_paid_course:
        raise HTTPException(status_code=404, detail="Course not found or it's not a paid course")

    # Create a Stripe payment intent
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(course.price * 100),  # Convert to cents
            currency='usd',
            metadata={'course_id': course_id, 'user_id': current_user.id}
        )

        # Save payment with status as 'pending' and store Stripe payment intent ID
        payment = Payment(
            user_id=current_user.id,
            course_id=course.id,
            amount=course.price,
            status="pending",
            stripe_payment_intent_id=intent['id']  # Store the Stripe payment intent ID
        )
        db.add(payment)
        db.commit()

        return {"client_secret": intent['client_secret'], "payment_id": payment.id}

    except CardError as e:
        # Card was declined
        raise HTTPException(status_code=400, detail=f"Card error: {e.user_message}")
    except RateLimitError as e:
        # Too many requests hit the API too quickly
        raise HTTPException(status_code=429, detail="Too many requests to Stripe. Please try again later.")
    except InvalidRequestError as e:
        # Invalid request (e.g., invalid parameters)
        raise HTTPException(status_code=400, detail=f"Invalid request: {e.user_message}")
    except AuthenticationError as e:
        # Authentication with Stripe's API failed
        raise HTTPException(status_code=401, detail="Authentication with payment provider failed")
    except APIConnectionError as e:
        # Network communication failed
        raise HTTPException(status_code=502, detail="Network error with payment provider")
    except StripeError as e:
        # Other general Stripe error
        raise HTTPException(status_code=500, detail="Something went wrong with the payment provider")
    except Exception as e:
        # Catch any other non-Stripe error
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/confirm-payment/")
def confirm_payment(payment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Retrieve the payment record using the local payment ID
    payment = db.query(Payment).filter(Payment.id == payment_id, Payment.user_id == current_user.id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    # Check Stripe payment status using the stored Stripe payment intent ID
    try:
        intent = stripe.PaymentIntent.retrieve(payment.stripe_payment_intent_id)  # Use Stripe payment intent ID

        # Check if additional action is required (e.g., 3D Secure authentication)
        if intent['status'] == 'requires_action':
            raise HTTPException(status_code=400, detail="Additional action required to complete the payment")

        # Check if payment was successful
        if intent['status'] == 'succeeded':
            # Update payment status
            payment.status = 'success'
            db.commit()

            return {"message": "Payment successful, please enroll in the course via the enrollment endpoint."}

        else:
            raise HTTPException(status_code=400, detail="Payment not successful")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving payment intent: {str(e)}")


