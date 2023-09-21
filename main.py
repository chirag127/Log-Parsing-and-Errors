# Import the necessary libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import pickle

# Load the log data from the CSV file
log_data = pd.read_csv('/workspaces/Log-Parsing-and-Errors/error.csv')

# Preprocess the log messages
# Data cleaning: remove any non-alphanumeric characters and convert to lowercase
log_data['_raw'] = log_data['_raw'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()

# Tokenization: split the messages into words
log_data['tokens'] = log_data['_raw'].str.split()

# Vectorization: transform the tokens into numerical vectors using TF-IDF
vectorizer = TfidfVectorizer(analyzer=lambda x: x) # Use the tokens as they are
X = vectorizer.fit_transform(log_data['tokens']) # X is a sparse matrix of shape (n_samples, n_features)

# Split the log data into training and testing datasets
# Use an 80-20 split, where 80% of the data goes to training and 20% to testing
train_size = int(0.8 * len(log_data)) # Calculate the number of samples for training
train_data = log_data[:train_size] # Select the first train_size samples for training
test_data = log_data[train_size:] # Select the remaining samples for testing

# Train a K-Means clustering model
# Pick an initial number of clusters, say 10, and adjust it later if needed
n_clusters = 10 # Number of clusters to start with
kmeans = KMeans(n_clusters=n_clusters, random_state=0) # Initialize the K-Means model with n_clusters and a random seed for reproducibility
kmeans.fit(X[:train_size]) # Train the model on the training data

# Save the trained K-Means model to a file for future use
filename = 'log_pattern_model.pkl' # File name to save the model
pickle.dump(kmeans, open(filename, 'wb')) # Save the model using pickle

# Set a minimum probability threshold for pattern matching, say 0.3, and change it later if needed
threshold = 0.3 # Minimum probability threshold for pattern matching

# Predict log patterns for the testing data
# Randomly select a few log messages from the testing data, say 5 messages to start
np.random.seed(0) # Set a random seed for reproducibility
sample_size = 5 # Number of messages to select randomly
sample_indices = np.random.choice(len(test_data), size=sample_size, replace=False) # Randomly select sample_size indices from the test data
sample_messages = test_data.iloc[sample_indices]['_raw'] # Select the corresponding messages from the test data

# For each test log message:
for message in sample_messages:
    # Compute the distances of the message to all cluster centers
    message_vector = vectorizer.transform([message]) # Transform the message into a vector using TF-IDF
    distances = euclidean_distances(message_vector, kmeans.cluster_centers_) # Compute the distances to all cluster centers using Euclidean distance

    # Find the cluster with the minimum distance
    min_distance = np.min(distances) # Find the minimum distance among all distances
    min_cluster = np.argmin(distances) # Find the cluster index that corresponds to the minimum distance

    # If the minimum distance is below the minimum probability threshold, assign the message to the cluster
    if min_distance < threshold:
        print(f'The message "{message}" belongs to cluster {min_cluster}')

    # If the minimum distance is above the threshold, create a new cluster for the message
    else:
        print(f'The message "{message}" does not match any existing cluster')
        n_clusters += 1 # Increment the number of clusters by 1
        kmeans.n_clusters = n_clusters # Update the number of clusters in the K-Means model
        kmeans.cluster_centers_ = np.append(kmeans.cluster_centers_, message_vector.toarray(), axis=0) # Append the message vector as a new cluster center

# Print out the cluster numbers for the training data
print(f'The cluster numbers for the training data are: {kmeans.labels_}')
