
import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# -------------------------------
# PROJECT: SPAM DETECTOR
# -------------------------------

st.set_page_config(
    page_title="Spam Detector AI",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ SPAM DETECTOR")
st.subheader("AI-Powered Spam and Fraud Detection")
st.write("Check suspicious messages, websites, job offers, payments and news.")

# -------------------------------
# TRAINING DATA
# -------------------------------

spam_messages = [
    "You won a lottery claim your prize now",
    "Congratulations you have won a free gift",
    "Click this link to claim your reward",
    "Send money to receive your prize",
    "Urgent your account will be blocked",
    "Verify your bank account immediately",
    "You have won a cash reward",
    "Limited offer buy now",
    "Get rich quickly with guaranteed returns",
    "Send your OTP to verify your account",
    "Your package is waiting pay delivery fee",
    "Earn thousands daily without any work",
    "Congratulations you are selected for a prize",
    "Pay registration fee to get this job",
    "Invest now for guaranteed profit",
    "Your account is suspended click here",
    "Claim your free mobile phone",
    "Send your personal details immediately",
    "You have received a special bonus",
    "Click here to unlock your account"
]

normal_messages = [
    "Hello how are you doing today",
    "Your school assignment is due tomorrow",
    "The meeting will start at ten",
    "Please call me when you are free",
    "Your order has been delivered",
    "Thank you for your purchase",
    "The class will begin at nine",
    "Please send me the homework",
    "Your appointment is confirmed",
    "I will meet you tomorrow",
    "The library is open today",
    "Your exam timetable is available",
    "Please check your email",
    "The project needs to be completed",
    "Have a nice day",
    "Your ticket booking is confirmed",
    "The office will remain closed tomorrow",
    "Please attend the online meeting",
    "Your payment was successful",
    "We will discuss this in class"
]

texts = spam_messages + normal_messages
labels = ["Spam"] * len(spam_messages) + ["Safe"] * len(normal_messages)

# -------------------------------
# TRAIN AI MODEL
# -------------------------------

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", MultinomialNB())
])

model.fit(texts, labels)

# -------------------------------
# DETECTION CATEGORIES
# -------------------------------

category = st.selectbox(
    "Choose what you want to check",
    [
        "SMS Spam",
        "Website Spam",
        "Fake Job",
        "Payment Fraud",
        "Fake News"
    ]
)

user_text = st.text_area(
    "Enter message, website link or information:",
    height=150,
    placeholder="Paste the text you want to check..."
)

# -------------------------------
# WARNING SIGN CHECKER
# -------------------------------

def find_warnings(text, category):
    warnings = []
    lower_text = text.lower()

    patterns = [
        (r"\b(otp|password|pin)\b", "Requests sensitive login information"),
        (r"\b(lottery|prize|winner|won)\b", "Unexpected prize or winning claim"),
        (r"\b(urgent|immediately|act now)\b", "Uses pressure or urgency"),
        (r"\b(guaranteed profit|double your money|get rich)\b",
         "Promises unrealistic financial returns"),
        (r"\b(registration fee|processing fee|pay fee)\b",
         "Requests an upfront fee"),
        (r"\b(click here|claim now|verify now)\b",
         "Encourages clicking or immediate action")
    ]

    for pattern, warning in patterns:
        if re.search(pattern, lower_text):
            warnings.append(warning)

    if category == "Website Spam":
        if re.search(r"https?://\d+\.\d+\.\d+\.\d+", text):
            warnings.append("Website uses an IP address instead of a normal domain")

        if re.search(r"bit\.ly|tinyurl\.com|t\.co", lower_text):
            warnings.append("Uses a shortened link")

    if category == "Fake News":
        if re.search(r"\b(shocking|secret|100% true|share immediately)\b", lower_text):
            warnings.append("Uses sensational or unverified-sounding language")

    return warnings

# -------------------------------
# DETECTION BUTTON
# -------------------------------

if st.button("🔍 CHECK NOW", use_container_width=True):

    if not user_text.strip():
        st.warning("Please enter some text first.")

    else:
        prediction = model.predict([user_text])[0]
        probabilities = model.predict_proba([user_text])[0]
        confidence = max(probabilities) * 100

        warnings = find_warnings(user_text, category)

        st.divider()
        st.subheader("Detection Result")

        if prediction == "Spam":
            st.error("⚠️ AI RESULT: POSSIBLE SPAM")
        else:
            st.success("✅ AI RESULT: LIKELY SAFE")

        st.write(f"**Model confidence:** {confidence:.1f}%")

        if warnings:
            st.subheader("Warning Signs")
            for warning in warnings:
                st.warning("⚠️ " + warning)
        else:
            st.info("No listed warning patterns were detected.")

        st.caption(
            "This is an educational prototype. "
            "It cannot confirm whether a message, website, job or news story is genuine."
        )

st.divider()
st.caption("Spam Detector AI | Python + Machine Learning")
