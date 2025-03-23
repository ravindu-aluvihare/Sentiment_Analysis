from flask import Flask, render_template, request, redirect, url_for
from helper import preprocessing, vectorizer, get_prediction
from logger import logging

app = Flask(__name__)

logging.info('✅ Flask server started successfully')

# Data store for reviews and sentiment counts
data = {
    "reviews": [],
    "positive": 0,
    "negative": 0
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if not text:
            logging.warning("⚠️ No text provided for sentiment analysis")
            return redirect(url_for('index'))

        logging.info(f"📝 Received Text: {text}")

        # Preprocessing
        preprocessed_txt = preprocessing(text)
        logging.info(f"🔍 Preprocessed Text: {preprocessed_txt}")

        # Vectorization
        vectorized_txt = vectorizer(preprocessed_txt)
        logging.info(f"📊 Vectorized Text: {vectorized_txt}")

        # Prediction
        prediction = get_prediction(vectorized_txt)
        logging.info(f"📈 Sentiment Prediction: {prediction}")

        # Update sentiment count
        if prediction == "negative":
            data["negative"] += 1
        else:
            data["positive"] += 1

        # Store latest review at the top
        data["reviews"].insert(0, text)

        return redirect(url_for("index"))

    logging.info("🏠 Opening Home Page")
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
