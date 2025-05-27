# Razorpay Integration Setup Guide

## Overview
This guide will help you set up Razorpay for your Rao Studios portfolio application.

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
3. Generate Live API Keys (ensure your account is activated)
4. Note down:
   - **Key ID** (starts with `rzp_live_` for production)
   - **Key Secret** (keep this confidential)

## Step 3: Configure Environment Variables in Render
Add these environment variables in your Render service:

```
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxx
```

**Important:**
- Use only `rzp_live_` keys for production
- Ensure your Razorpay account is activated for live transactions
- Never use test keys in production environment

## Step 4: Deploy and Verify
1. Deploy your application to Render with live keys
2. Ensure all environment variables are properly set
3. Test with real payment methods (small amounts recommended for initial testing)

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

### Configuration Check
Verify in your Render dashboard that:
- RAZORPAY_KEY_ID is set with live key (starts with rzp_live_)
- RAZORPAY_KEY_SECRET is set correctly
- Application logs show successful Razorpay client initialization

## Security Notes
- Never expose your Key Secret in frontend code
- Always verify payment signatures on the server
- Use HTTPS in production
- Keep your API credentials secure

## Support
- Razorpay Documentation: [docs.razorpay.com](https://docs.razorpay.com)
- Razorpay Support: [support.razorpay.com](https://support.razorpay.com)
