# Import the necessary libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import pickle

def my_print(x):
    # my_print(x)
    pass


# Load the log data from the CSV file
log_data = pd.read_csv('/workspaces/Log-Parsing-and-Errors/error.csv')

# remove all the columns except the message column i.e. _raw

log_data = log_data[['_raw']]

# Preprocess the log messages
# Data cleaning: remove any non-alphanumeric characters and convert to lowercase
log_data['_raw'] = log_data['_raw'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()

## randomise the order of the log messages
log_data = log_data.sample(frac=1).reset_index(drop=True)

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

# Determine the optimal number of clusters using the Elbow Method
# You can adjust the range of cluster numbers as needed
wcss = []  # Within-cluster sum of squares
max_clusters = 10  # Maximum number of clusters to consider
for i in range(1, max_clusters + 1):
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(X[:train_size])
    wcss.append(kmeans.inertia_)

# Find the "elbow" point in the plot
elbow_point = None
for i in range(1, len(wcss) - 1):
    if (wcss[i] - wcss[i + 1]) / (wcss[i - 1] - wcss[i]) > 0.1:
        elbow_point = i + 1
        break

if elbow_point is None:
    elbow_point = 1  # Default to 1 cluster if no clear elbow point

# Train the final K-Means model with the determined number of clusters
n_clusters = 5  # Number of clusters determined by the Elbow Method
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
kmeans.fit(X[:train_size])

# Save the trained K-Means model to a file for future use
filename = 'log_pattern_model.pkl'  # File name to save the model
pickle.dump(kmeans, open(filename, 'wb'))  # Save the model using pickle

# Set a minimum probability threshold for pattern matching, say 0.3, and change it later if needed
threshold = 0.3  # Minimum probability threshold for pattern matching

# Predict log patterns for the testing data
# Randomly select a few log messages from the testing data, say 5 messages to start
np.random.seed(0)  # Set a random seed for reproducibility
sample_size = 5  # Number of messages to select randomly
sample_indices = np.random.choice(len(test_data), size=sample_size, replace=False)  # Randomly select sample_size indices from the test data
sample_messages = test_data.iloc[sample_indices]['_raw']  # Select the corresponding messages from the test data

# For each test log message:
for message in sample_messages:
    # Compute the distances of the message to all cluster centers
    message_vector = vectorizer.transform([message])  # Transform the message into a vector using TF-IDF
    distances = euclidean_distances(message_vector, kmeans.cluster_centers_)  # Compute the distances to all cluster centers using Euclidean distance

    # Find the cluster with the minimum distance
    min_distance = np.min(distances)  # Find the minimum distance among all distances
    min_cluster = np.argmin(distances)  # Find the cluster index that corresponds to the minimum distance

    # If the minimum distance is below the minimum probability threshold, assign the message to the cluster
    if min_distance < threshold:
        my_print(f'The message "{message}" belongs to cluster {min_cluster}')

    # If the minimum distance is above the threshold, create a new cluster for the message
    else:
        my_print(f'The message "{message}" does not match any existing cluster')
        n_clusters += 1  # Increment the number of clusters by 1
        kmeans.n_clusters = n_clusters  # Update the number of clusters in the K-Means model
        kmeans.cluster_centers_ = np.append(kmeans.cluster_centers_, message_vector.toarray(), axis=0)  # Append the message vector as a new cluster center

# Print out the cluster numbers for the training data
my_print(f'The cluster numbers for the training data are: {kmeans.labels_}')


# Print out the two example of each cluster
for i in range(n_clusters):
    try:
        print(f'Cluster {i}:')
        print(log_data.iloc[np.where(kmeans.labels_ == i)[0][0]]['_raw'])
        print('the second one')
        print(log_data.iloc[np.where(kmeans.labels_ == i)[0][1]]['_raw'])

        print('')
    except:
        pass