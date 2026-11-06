
import streamlit as st
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# ==========================================
# SPAM DETECTOR AI - PROFESSIONAL EDITION
# ==========================================

st.set_page_config(
    page_title="Spam Detector AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #080d20,
        #101b38,
        #17132e
    );
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #101a35,
        #17112e
    );
}

h1, h2, h3 {
    color: #ffffff !important;
}

p, label, li {
    color: #d8e2ff;
}

.hero {
    background: linear-gradient(
        120deg,
        #172b59,
        #42276e,
        #123b59
    );
    padding: 35px;
    border-radius: 22px;
    border: 1px solid #536da8;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 17px;
}

.card {
    background: linear-gradient(
        145deg,
        #192748,
        #241b42
    );
    padding: 23px;
    border-radius: 17px;
    border: 1px solid #344c78;
    min-height: 145px;
    margin-bottom: 12px;
}

.card h2 {
    font-size: 30px;
}

.card p {
    color: #c3d1f5;
}

.result {
    background: #172b42;
    border: 1px solid #4382b9;
    border-radius: 16px;
    padding: 22px;
    margin-top: 15px;
}

.small-title {
    color: #8eb8ff;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 2px;
}

div.stButton > button {
    background: linear-gradient(
        90deg,
        #3867ff,
        #8b48e8
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-weight: bold;
}

div.stButton > button:hover {
    border: 1px solid white;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# MACHINE LEARNING DATA
# ==========================================

spam_data = [
    "You won a lottery claim your prize",
    "Click here to get free money",
    "Send your OTP immediately",
    "Your bank account will be blocked",
    "Claim your free gift now",
    "You are a lucky winner",
    "Pay registration fee to get job",
    "Earn thousands without working",
    "Guaranteed profit invest now",
    "Double your money today",
    "Your account is suspended verify now",
    "Send your password to claim reward",
    "Congratulations you won a cash prize",
    "Urgent payment required immediately",
    "Get rich quickly with our scheme",
    "Click this link to claim reward",
    "You have received a free mobile",
    "Pay processing fee to receive prize",
    "Your account needs immediate verification",
    "Exclusive offer claim now"
]

safe_data = [
    "Hello how are you today",
    "Your school assignment is due tomorrow",
    "The meeting starts at ten",
    "Please call me when you are free",
    "Your order has been delivered",
    "Thank you for your purchase",
    "The class begins at nine",
    "Please send me the homework",
    "Your appointment is confirmed",
    "I will meet you tomorrow",
    "The library is open today",
    "Your exam timetable is available",
    "Please check your email",
    "The project is completed",
    "Have a nice day",
    "Your ticket booking is confirmed",
    "The office is closed tomorrow",
    "Please attend the online meeting",
    "Your payment was successful",
    "We will discuss this in class"
]

training_text = spam_data + safe_data
training_labels = (
    ["Spam"] * len(spam_data)
    + ["Safe"] * len(safe_data)
)

model = Pipeline([
    ("vectorizer", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", MultinomialNB())
])

model.fit(training_text, training_labels)

# ==========================================
# EXAMPLES
# ==========================================

examples = {
    "SMS Spam": "Congratulations! You won a free prize. Click here to claim now.",
    "Website Spam": "Visit http://192.168.1.1 and claim your free reward now.",
    "Fake Job": "Earn thousands daily. Pay registration fee to get this job.",
    "Payment Fraud": "Your bank account is blocked. Send your OTP immediately.",
    "Fake News": "Shocking news! Share immediately. This secret information is 100% true."
}

# ==========================================
# WARNING CHECKER
# ==========================================

def check_warnings(text, category):

    warnings = []
    lower = text.lower()

    patterns = [
        (r"\b(otp|password|pin)\b",
         "Requests sensitive login information"),

        (r"\b(lottery|prize|winner|won)\b",
         "Unexpected prize or winning claim"),

        (r"\b(urgent|immediately|act now)\b",
         "Uses urgency to pressure the user"),

        (r"\b(guaranteed profit|double your money|get rich)\b",
         "Promises unrealistic financial returns"),

        (r"\b(registration fee|processing fee|pay fee)\b",
         "Requests an upfront fee"),

        (r"\b(click here|claim now|verify now)\b",
         "Encourages immediate clicking or action")
    ]

    for pattern, warning in patterns:
        if re.search(pattern, lower):
            warnings.append(warning)

    if category == "Website Spam":

        if re.search(r"https?://\d+\.\d+\.\d+\.\d+", lower):
            warnings.append("URL contains an IP address")

        if re.search(r"bit\.ly|tinyurl\.com|t\.co", lower):
            warnings.append("Shortened website link detected")

    if category == "Fake News":

        if re.search(r"\b(shocking|secret|share immediately)\b", lower):
            warnings.append("Sensational language detected")

    if category == "Fake Job":

        if re.search(r"\b(no experience|easy money|work from home)\b", lower):
            warnings.append("Job offer uses claims that need verification")

    return warnings

# ==========================================
# SIDEBAR MENU
# ==========================================

st.sidebar.markdown("# 🛡️ SPAM AI")
st.sidebar.caption("SMART DIGITAL PROTECTION")
st.sidebar.divider()

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "🏠 Home",
        "🔍 AI Detector",
        "🧪 Try Examples",
        "📊 Statistics",
        "ℹ️ About Project"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### 🛡️ Protection Center")
st.sidebar.success("AI Model Loaded")

st.sidebar.caption(
    "Spam Detector AI | Python + Machine Learning"
)

# ==========================================
# HOME PAGE
# ==========================================

if page == "🏠 Home":

    st.markdown("""
    <div class="hero">
        <div class="small-title">ARTIFICIAL INTELLIGENCE PROJECT</div>
        <h1>🛡️ SPAM DETECTOR AI</h1>
        <p>
        Detect suspicious messages, websites and
        online content using Machine Learning.
        </p>
        <h3>Think Smart. Stay Safe. Stay Protected.</h3>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Welcome to your Security Dashboard")

    st.write(
        "Explore the features of Spam Detector AI "
        "and learn how machine learning can identify "
        "common online warning signs."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h2>📱</h2>
        <h3>SMS Detection</h3>
        <p>Check suspicious text messages.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h2>🌐</h2>
        <h3>Website Detection</h3>
        <p>Check links for warning signs.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h2>💼</h2>
        <h3>Job Detection</h3>
        <p>Check suspicious job offers.</p>
        </div>
        """, unsafe_allow_html=True)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
        <div class="card">
        <h2>💳</h2>
        <h3>Payment Fraud</h3>
        <p>Identify suspicious payment requests.</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="card">
        <h2>📰</h2>
        <h3>Fake News Warning</h3>
        <p>Identify suspicious news language.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("How It Works")

    a, b, c = st.columns(3)

    a.info("**01 — ENTER**\n\nEnter your text or link.")
    b.info("**02 — ANALYSE**\n\nAI checks the text.")
    c.success("**03 — RESULT**\n\nSee possible warning signs.")

    st.markdown("""
    <div class="hero">
        <h2>🔐 Your Digital Safety Matters</h2>
        <p>
        Always think before clicking unknown links
        or sharing personal information.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# AI DETECTOR PAGE
# ==========================================

elif page == "🔍 AI Detector":

    st.title("🔍 AI Spam Detector")

    st.write(
        "Select a category and enter the text "
        "you want the AI model to analyse."
    )

    category = st.selectbox(
        "Select Detection Category",
        list(examples.keys())
    )

    st.markdown("### Enter Your Content")

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    if st.button("Load Sample Example"):
        st.session_state.user_input = examples[category]

    user_text = st.text_area(
        "Paste your message, link or information:",
        key="user_input",
        height=170,
        placeholder="Enter your text here..."
    )

    if st.button("🚀 ANALYSE NOW", use_container_width=True):

        if not user_text.strip():

            st.warning("Please enter some text first.")

        else:

            prediction = model.predict([user_text])[0]

            probabilities = model.predict_proba([user_text])[0]

            classes = model.classes_

            spam_probability = probabilities[
                list(classes).index("Spam")
            ]

            warnings = check_warnings(user_text, category)

            st.divider()
            st.subheader("📋 Analysis Results")

            if prediction == "Spam" or warnings:

                st.error("⚠️ POSSIBLY SUSPICIOUS")

            else:

                st.success("✅ LIKELY SAFE")

            st.markdown(
                f'<div class="result"><h3>🤖 AI Classification: '
                f'{prediction}</h3><p>Model spam score: '
                f'{spam_probability * 100:.1f}%</p></div>',
                unsafe_allow_html=True
            )

            st.progress(float(spam_probability))

            if warnings:

                st.subheader("⚠️ Warning Signs")

                for warning in warnings:
                    st.warning(warning)

            else:

                st.info("No listed warning patterns were detected.")

            st.caption(
                "The model score is not a verified probability "
                "of fraud. This educational tool cannot confirm "
                "whether content is genuine."
            )

# ==========================================
# TRY EXAMPLES PAGE
# ==========================================

elif page == "🧪 Try Examples":

    st.title("🧪 Try Sample Examples")

    st.write(
        "Explore sample messages and learn how "
        "the Spam Detector AI works."
    )

    for name, example in examples.items():

        with st.expander(name):

            st.code(example, language="text")

            st.write(
                "Copy this example and paste it into "
                "the AI Detector page to test it."
            )

    st.info(
        "These examples are created for educational "
        "demonstrations."
    )

# ==========================================
# STATISTICS PAGE
# ==========================================

elif page == "📊 Statistics":

    st.title("📊 Project Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Training Examples", len(training_text))
    col2.metric("Spam Examples", len(spam_data))
    col3.metric("Safe Examples", len(safe_data))

    st.subheader("Training Dataset")

    chart_data = pd.DataFrame({
        "Category": ["Spam", "Safe"],
        "Examples": [len(spam_data), len(safe_data)]
    })

    st.bar_chart(
        chart_data.set_index("Category")
    )

    st.caption(
        "These figures describe the sample training data, "
        "not real-world detection performance."
    )

    st.subheader("Detection Categories")

    st.write("📱 SMS Spam")
    st.write("🌐 Website Spam")
    st.write("💼 Fake Job")
    st.write("💳 Payment Fraud")
    st.write("📰 Fake News")

# ==========================================
# ABOUT PROJECT PAGE
# ==========================================

elif page == "ℹ️ About Project":

    st.title("ℹ️ About Spam Detector AI")

    st.markdown("""
    <div class="hero">
        <h1>🛡️ Spam Detector AI</h1>
        <p>
        An educational Artificial Intelligence
        and Machine Learning project.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Project Objective")

    st.write(
        "The objective is to demonstrate how machine "
        "learning can classify text and identify common "
        "warning signs in online content."
    )

    st.subheader("Technologies Used")

    st.write("🐍 Python")
    st.write("🤖 Scikit-learn")
    st.write("📊 TF-IDF Vectorizer")
    st.write("🧠 Multinomial Naive Bayes")
    st.write("🌐 Streamlit")
    
    st.subheader("Five Main Features")

    for item in examples:
        st.write("✅ " + item)

    st.warning(
        "This is a beginner educational prototype. "
        "It cannot independently verify websites, "
        "jobs, payment transactions or news. "
        "Never enter real passwords, OTPs or bank details."
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <h3>🛡️ SPAM DETECTOR AI</h3>
        <p>Built with Python and Machine Learning</p>
        <p>Educational AI Project | 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)
