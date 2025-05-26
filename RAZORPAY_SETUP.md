# Razorpay Integration Setup Guide

## Overview
Your Flask application has been successfully migrated from PayU to Razorpay payment gateway. This guide will help you set up Razorpay for your Rao Studios portfolio application.

## Prerequisites
- Razorpay merchant account
- Access to Render dashboard for environment variables

## Step 1: Create Razorpay Account
1. Visit [razorpay.com](https://razorpay.com)
2. Sign up for a merchant account
3. Complete the KYC verification process
4. Wait for account activation (usually 24-48 hours)

## Step 2: Get API Credentials
1. Login to your Razorpay Dashboard
2. Go to **Settings** → **API Keys**
3. Generate API Keys (if not already generated)
4. Note down:
   - **Key ID** (starts with `rzp_test_` for test mode)
   - **Key Secret** (keep this confidential)

## Step 3: Configure Environment Variables in Render
Add these environment variables in your Render service:

```
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxx
```

**For Production:**
- Use `rzp_live_` keys instead of `rzp_test_`
- Ensure your Razorpay account is activated for live transactions

## Step 4: Test the Integration
1. Deploy your application to Render
2. Visit `/test-payment` endpoint to check configuration
3. Try making a test booking with ₹1 payment

## Test Cards (for Test Mode)
Use these test card details for testing:

**Successful Payment:**
- Card Number: `4111 1111 1111 1111`
- Expiry: Any future date
- CVV: Any 3 digits

**Failed Payment:**
- Card Number: `4000 0000 0000 0002`
- Expiry: Any future date
- CVV: Any 3 digits

## Features Implemented
✅ Razorpay Checkout integration
✅ Order creation and payment capture
✅ Payment signature verification
✅ Success/failure handling
✅ Email notifications
✅ Booking status updates
✅ Mobile-responsive payment UI
✅ Support for all payment methods (Cards, UPI, Net Banking, Wallets)

## Payment Flow
1. User fills booking form
2. Booking record created with 'pending' status
3. User redirected to booking confirmation page
4. User clicks "Pay Now" button
5. Razorpay checkout modal opens
6. User completes payment
7. Payment verified and booking status updated to 'completed'
8. Confirmation email sent

## Troubleshooting

### Payment System Unavailable
- Check if `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` are set
- Verify the credentials are correct
- Check Render logs for any errors

### Payment Verification Failed
- Ensure webhook signature verification is working
- Check if the order ID matches
- Verify the payment amount

### Test Endpoint
Visit `https://your-app.onrender.com/test-payment` to check:
- Configuration status
- Test order creation
- API connectivity

## Security Notes
- Never expose your Key Secret in frontend code
- Always verify payment signatures on the server
- Use HTTPS in production
- Keep your API credentials secure

## Support
- Razorpay Documentation: [docs.razorpay.com](https://docs.razorpay.com)
- Razorpay Support: [support.razorpay.com](https://support.razorpay.com)

## Migration Complete ✅
Your application has been successfully migrated from PayU to Razorpay with all the necessary features and security measures in place. 