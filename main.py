import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import tkinter as tk


class Scraper:
    def __init__(self, url):
        self.url = url

    def scrape_website(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()


class SentimentAnalyzer:
    def __init__(self, text):
        self.text = text

    def analyze_sentiment(self):
        blob = TextBlob(self.text)
        sentiment_polarity = blob.sentiment.polarity
        if sentiment_polarity > 0:
            return "Positive"
        elif sentiment_polarity < 0:
            return "Negative"
        else:
            return "Neutral"


class ModelTrainer:
    def __init__(self, dataset):
        self.dataset_path = dataset
        self.features = []
        self.labels = []

    def load_dataset(self):
        dataset = pd.read_csv(self.dataset_path)
        self.features = dataset.iloc[:, :-1].values
        self.labels = dataset.iloc[:, -1].values

    def train_model(self):
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.labels, test_size=0.2, random_state=42)
        classifier = RandomForestClassifier()
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy


class InvestmentReport:
    def __init__(self, insights):
        self.insights = insights

    def generate_report(self):
        report = f"Investment Insights:\n{'-' * 20}\n"
        for insight in self.insights:
            report += f"- {insight}\n"
        return report


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Investment Opportunities")

        self.url_label = tk.Label(self.window, text="Website URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.window, width=50)
        self.url_entry.pack()

        self.scrape_button = tk.Button(self.window, text="Scrape", command=self.scrape_website)
        self.scrape_button.pack()

        self.sentiment_label = tk.Label(self.window, text="Sentiment:")
        self.sentiment_label.pack()

        self.sentiment_result = tk.Label(self.window, text="")
        self.sentiment_result.pack()

        self.report_label = tk.Label(self.window, text="Investment Report:")
        self.report_label.pack()

        self.report_text = tk.Text(self.window, height=10, width=50)
        self.report_text.pack()

        self.window.mainloop()

    def scrape_website(self):
        url = self.url_entry.get()
        scraper = Scraper(url)
        content = scraper.scrape_website()
        analyzer = SentimentAnalyzer(content)
        sentiment = analyzer.analyze_sentiment()
        self.sentiment_result.configure(text=sentiment)
        self.generate_report(content, sentiment)

    def generate_report(self, content, sentiment):
        model = ModelTrainer("dataset.csv")
        model.load_dataset()
        accuracy = model.train_model()
        insights = [f"Sentiment: {sentiment}", f"Accuracy: {accuracy}"]
        report = InvestmentReport(insights)
        report_text = report.generate_report()
        self.report_text.insert(tk.END, report_text)


if __name__ == "__main__":
    gui = GUI()