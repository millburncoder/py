import streamlit as st
import random
from textblob import TextBlob


# Stubbed API calls
def check_order_details(order_number, email_or_zip):
    """
    API call to check order details.
    Replace with actual implementation.
    """
    # Simulating response
    if order_number == "12345" and email_or_zip in ["user@example.com", "67890"]:
        return {"status": "success", "details": {"order_number": order_number, "email_or_zip": email_or_zip}}
    else:
        return {"status": "error", "message": "Order not found"}


def check_return_or_exchange_eligibility(order_number):
    """
    API call to check eligibility for return or exchange.
    Replace with actual implementation.
    """
    # Simulating response
    return {"eligible": True, "exchange_available": random.choice([True, False])}


def get_exchange_inventory(order_number):
    """
    API call to get inventory details for an exchange.
    Replace with actual implementation.
    """
    # Simulating inventory options
    return {"available": True, "options": ["Red (M)", "Red (L)", "Blue (M)", "Blue (L)"]}


def generate_return_label_api(order_number):
    """
    API call to generate a return label.
    Replace with actual implementation.
    """
    # Simulating response
    tracking_number = f"1Z{order_number[-6:]}1234567890"
    label_url = f"https://example.com/labels/{tracking_number}.pdf"
    return {"tracking_number": tracking_number, "label_url": label_url}


# Sentiment analysis function
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score < 0:
        return "negative"
    elif sentiment_score > 0:
        return "positive"
    else:
        return "neutral"


# Streamlit chatbot
st.title("🎥 Chatbot: Returns and Refunds")
st.write("Describe your issue, and we’ll help you with your return or refund.")

# Step 1: Free-form input
user_input = st.text_area("What's the issue with your order?")

if user_input:
    sentiment = analyze_sentiment(user_input)
    if sentiment == "negative":
        st.warning("We're sorry to hear about your experience. Let's make it right!")
    elif sentiment == "positive":
        st.success("Thank you for sharing your feedback! Let’s proceed with your request.")
    else:
        st.info("Thank you for your input. Let’s proceed with your request.")

    # Step 2: Order number input
    order_number = st.text_input("Please provide your order number:")
    if order_number:
        email_or_zip = st.text_input("Please provide your email address or billing ZIP code:")
        if email_or_zip:
            # Validate order details via API
            order_details_response = check_order_details(order_number, email_or_zip)
            if order_details_response["status"] == "error":
                st.error(order_details_response["message"])
            else:
                st.success("Order details validated!")

                # Check eligibility for return or exchange
                eligibility_response = check_return_or_exchange_eligibility(order_number)
                if not eligibility_response["eligible"]:
                    st.error("This order is not eligible for a return or exchange.")
                else:
                    if eligibility_response["exchange_available"]:
                        # Fetch exchange inventory
                        inventory_response = get_exchange_inventory(order_number)
                        if inventory_response["available"]:
                            st.info("An exchange is available for your item!")
                            options = inventory_response["options"]
                            selected_option = st.radio("Choose an exchange option:", options)
                            if st.button("Confirm Exchange"):
                                st.success(f"Your exchange request for {selected_option} has been processed.")

                                # Generate return label for the exchange
                                label_response = generate_return_label_api(order_number)
                                st.success(
                                    f"A return label has been generated! Tracking Number: {label_response['tracking_number']}.")
                                st.markdown(f"[Download Return Label]({label_response['label_url']})")
                        else:
                            st.error("Exchange options are currently unavailable.")
                    else:
                        st.warning("No exchange is available. Proceeding with refund.")

                        # Step 3: Refund flow
                        is_damaged = st.radio("Is the item worn or damaged?", ["Yes", "No"])
                        if is_damaged == "Yes":
                            loyalty_member = st.radio("Are you a loyalty member?", ["Yes", "No"])
                            if loyalty_member == "Yes" and st.button("Confirm Refund"):
                                st.success(
                                    "You can keep the item. A refund will be processed to your original payment method in 5-10 days.")
                            elif st.button("Confirm Return for Refund"):
                                # Generate return label for refund
                                label_response = generate_return_label_api(order_number)
                                if label_response:
                                    st.success(
                                        f"Your return label has been generated! Tracking Number: {label_response['tracking_number']}.")
                                    st.markdown(f"[Download Return Label]({label_response['label_url']})")
                                else:
                                    st.error("Unable to generate return label. Please contact customer support.")
                        elif is_damaged == "No" and st.button("Confirm Refund"):
                            st.success("A refund will be processed to your original payment method in 5-10 days.")
