import pandas as pd

# Define the error examples, regex patterns, and error solutions for each cluster
cluster_data = [
    {
        "Error Regex": r"cookie header was received.*invalid cookie",
        "Error Solution": "Ignore the invalid cookie in the received header.",
    },
    {
        "Error Regex": r"servlet.service\(\) for servlet \[dispatcherservlet\] threw exception",
        "Error Solution": "Handle the exception thrown by the servlet service.",
    },
    {
        "Error Regex": r"discoveryclient.*unable to send heartbeat",
        "Error Solution": "Investigate and resolve the issue related to sending heartbeat.",
    },
    {
        "Error Regex": r"exception processing errorpage\[errorcode=\d+.*location=\/error\]",
        "Error Solution": "Handle the exception in the error processing code.",
    },
    {
        "Error Regex": r'request execution failed with message: i/o error on put request for "".*connect to .* failed: connection refused',
        "Error Solution": "Investigate the connection issue to the specified host.",
    },
    {
        "Error Regex": r'request execution failed with message: i/o error on get request for "".*connect to .* failed: connection refused',
        "Error Solution": "Investigate the connection issue to the specified host.",
    },
    {
        "Error Regex": r'request execution failed with message: i/o error on put request for "".*connect to .* failed: connection refused',
        "Error Solution": "Investigate the connection issue to the specified host.",
    },
]

# Create a DataFrame from the cluster_data
df = pd.DataFrame(cluster_data)

# Save the DataFrame to a CSV file
df.to_csv("cluster_error_data.csv", index=False)
