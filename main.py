import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re


# Load the log data from the CSV file (replace with your own dataset path)
log_data = pd.read_csv("/workspaces/Log-Parsing-and-Errors/error.csv")

# Keep only the '_raw' column
log_data = log_data[["_raw"]]


# # for each log message, remove the log messages which don't contain "ERROR" in the first 100 characters
# for i in range(len(log_data)):
#     if "ERROR" not in log_data["_raw"][i][:100]:
#         log_data = log_data.drop(i)

# Reset the index
log_data = log_data.reset_index(drop=True)


# for each log message, remove the everything before the third :
for i in range(len(log_data)):
    log_data["_raw"][i] = log_data["_raw"][i].split(":", 3)[-1]


# for each log message, truncate the log messages after the first 100 characters

for i in range(len(log_data)):
    log_data["_raw"][i] = log_data["_raw"][i][:500]


# for each log message, remove everything after the first line break character
for i in range(len(log_data)):
    log_data["_raw"][i] = log_data["_raw"][i].split("\n", 1)[0]


# Data preprocessing: remove non-alphanumeric characters and convert to lowercase
log_data["_raw"] = log_data["_raw"].str.replace("[^a-zA-Z0-9 ]", "").str.lower()

# Define a regular expression pattern to match URLs
url_pattern = (
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


# Function to remove URLs from a text
def remove_urls(text):
    return re.sub(url_pattern, "", text)


# Apply the remove_urls function to each log message
log_data["_raw"] = log_data["_raw"].apply(remove_urls)

data = {
    "log_message": log_data["_raw"].tolist(),
}

df = pd.DataFrame(data)


# Vectorize log messages using TF-IDF
vectorizer = TfidfVectorizer(max_features=500, stop_words="english")
log_vectors = vectorizer.fit_transform(df["log_message"])


# Calculate WCSS for different values of k
# wcss = []
# for k in range(1, 21):  # You can adjust the range as needed
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(log_vectors)
#     wcss.append(kmeans.inertia_)

# # Find the optimal number of clusters (k)
# optimal_k = None
# for i in range(1, len(wcss)):
#     slope = (wcss[i] - wcss[i - 1]) / 2  # Calculate the slope of the WCSS curve
#     if slope < 100:  # You can adjust this threshold based on your data
#         optimal_k = i + 1  # +1 because we started from k=1
#         break


# Train a K-Means clustering model
n_clusters = 5  # You can adjust the number of clusters as needed
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(log_vectors)

# Extract keywords from cluster centroids
cluster_keywords = {}
for cluster_id in range(n_clusters):
    # Get indices of log messages in this cluster
    cluster_indices = kmeans.labels_ == cluster_id

    # Extract keywords from the log messages in this cluster
    keywords = []
    for log_message in df.loc[cluster_indices, "log_message"]:
        keywords += re.findall(r"\b\w+\b", log_message)

    # Count and rank keyword occurrences
    keyword_counts = pd.Series(keywords).value_counts()

    # Store the top keywords for this cluster
    cluster_keywords[cluster_id] = keyword_counts.index.tolist()[
        :5
    ]  # Adjust the number of keywords as needed

# Print the identified patterns (top keywords for each cluster)
print("Identified Patterns:")
for cluster_id, keywords in cluster_keywords.items():
    print(f"Pattern {cluster_id + 1}: {', '.join(keywords)}")


# make a list of one message per cluster
cluster_messages = []
for cluster_id in range(n_clusters):
    # Get indices of log messages in this cluster
    cluster_indices = kmeans.labels_ == cluster_id

    # Extract keywords from the log messages in this cluster
    keywords = []
    for log_message in df.loc[cluster_indices, "log_message"]:
        keywords += re.findall(r"\b\w+\b", log_message)

    # Count and rank keyword occurrences
    keyword_counts = pd.Series(keywords).value_counts()

    # Store the top keywords for this cluster
    cluster_messages.append(df.loc[cluster_indices, "log_message"].tolist()[0])


# print(cluster_messages)
for message in cluster_messages:
    print(f"cluster number: {cluster_messages.index(message) + 1} \n {message} \n")
# Replace 'YOUR_API_KEY' with your CohereAI API key
import cohere

co = cohere.Client(
    "PQ50WPjjMsFSzUhZlMQaGTlS30MyRs9YkbuKfhHh"
)  # This is your trial API key


def generate_patterns(log_messages, num_patterns=5):
    patterns = []

    # Iterate through log messages
    for message in log_messages:
        response = co.chat(
            model="command-nightly",
            message=f"Please generate a regex pattern to match the following log message: {message}\n\nonly give regex and nothing else strictly",
            temperature=0.3,
            #   chat_history=[{"user_name": "User", "message": f"Please generate a regex pattern to match the following log message: {message}\n\nonly give regex and nothing else strictly"}],
            prompt_truncation="auto",
            # stream=True,
            citation_quality="accurate",
            connectors=[{"id": "web-search"}],
        )
        # print(response)
        generated_patterns = response.text
        print("Prediction: {}".format(generated_patterns))
        # Extract generated patterns from the response

        patterns.append({"log_message": message, "patterns": generated_patterns})

    return patterns


# Generate patterns for each cluster
cluster_patterns = generate_patterns(cluster_messages)

# Print the identified patterns (top keywords for each cluster)
print("Identified Patterns:")
for cluster_id, patterns in enumerate(cluster_patterns):
    print(f"Pattern {cluster_id + 1}: {patterns['patterns']}")
