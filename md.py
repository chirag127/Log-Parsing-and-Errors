import pandas as pd

# Define the error examples, regex patterns, and error solutions for each cluster
cluster_data = [
    {
        "Cluster": 1,
        "Error Example": "a cookie header was received [${jndi:ldap://log4shell-generic-8molyf0ab2aqtscsyugh${lower:ten}.w.nessus.org/nessus}=${jndi:ldap://log4shell-generic-8molyf0ab2aqtscsyugh${lower:ten}.w.nessus.org/nessus};]",
        "Error Regex": r"cookie header was received.*invalid cookie",
        "Error Solution": "Ignore the invalid cookie in the received header.",
    },
    {
        "Cluster": 2,
        "Error Example": "servlet.service() for servlet [dispatcherservlet] in context with path [] threw exception",
        "Error Regex": r"servlet.service\(\) for servlet \[dispatcherservlet\] threw exception",
        "Error Solution": "Handle the exception thrown by the servlet service.",
    },
    {
        "Cluster": 3,
        "Error Example": "discoveryclient_rdd-async-service/p1049433.prod.cloud.fedex.com:rdd-async-service:6521 - was unable to send heartbeat!",
        "Error Regex": r"discoveryclient.*unable to send heartbeat",
        "Error Solution": "Investigate and resolve the issue related to sending heartbeat.",
    },
    {
        "Cluster": 4,
        "Error Example": "exception processing errorpage[errorcode=0, location=/error]",
        "Error Regex": r"exception processing errorpage\[errorcode=\d+.*location=\/error\]",
        "Error Solution": "Handle the exception in the error processing code.",
    },
    {
        "Cluster": 5,
        "Error Example": 'request execution failed with message: i/o error on put request for "": connect to rddgwslas03.prod.cloud.fedex.com:8094 [rddgwslas03.prod.cloud.fedex.com/10.228.54.50] failed: connection refused (connection refused); nested exception is org.apache.http.conn.httphostconnectexception: connect to rddgwslas03.prod.cloud.fedex.com:8094 [rddgwslas03.prod.cloud.fedex.com/10.2',
        "Error Regex": r'request execution failed with message: i/o error on put request for "".*connect to .* failed: connection refused',
        "Error Solution": "Investigate the connection issue to the specified host.",
    },
    {
        "Cluster": 6,
        "Error Example": 'request execution failed with message: i/o error on get request for "": connect to rddgwsatl04.prod.cloud.fedex.com:8094 [rddgwsatl04.prod.cloud.fedex.com/10.52.77.32] failed: connection refused (connection refused); nested exception is org.apache.http.conn.httphostconnectexception: connect to rddgwsatl04.prod.cloud.fedex.com:8094 [rddgwsatl04.prod.cloud.fedex.com/10.52.77.32] failed: connection refused (connection refused)',
        "Error Regex": r'request execution failed with message: i/o error on get request for "".*connect to .* failed: connection refused',
        "Error Solution": "Investigate the connection issue to the specified host.",
    },
    {
        "Cluster": 7,
        "Error Example": 'request execution failed with message: i/o error on put request for "": connect to rddgwsatl02.prod.cloud.fedex.com:8094 [rddgwsatl02.prod.cloud.fedex.com/10.52.172.30] failed: connection refused (connection refused); nested exception is org.apache.http.conn.httphostconnectexception: connect to rddgwsatl02.prod.cloud.fedex.com:8094 [rddgwsatl02.prod.cloud.fedex.com/10.5',
        "Error Regex": r'request execution failed with message: i/o error on put request for "".*connect to .* failed: connection refused',
        "Error Solution": "Investigate the connection issue to the specified host.",
    },
]

# Create a DataFrame from the cluster_data
df = pd.DataFrame(cluster_data)

# Save the DataFrame to a CSV file
df.to_csv("cluster_error_data.csv", index=False)
