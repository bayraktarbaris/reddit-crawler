# reddit-crawler

## Installation:

pip install -r requirements.txt

## Run

For writing Parquet files:\
```bin/write```

Files are located in ```data``` folder which is under project root.

For reading Parquet files:\
```bin/read```

## Comments

1. I didn't add any data cleanup because I am not in this data domain. However, as I commented in services, we can clean
   comments if ```"author": "[deleted]" or "body": "[removed]"```, and submissions if ```"author": "[deleted]"```
2. I tried to add unit tests to write parquet files for already downloaded data, but it added more complexity to the
   codebase since I should add wrapper class for "spark sqlContext".
3. Also, I tried to add unit tests for Pushshift API but since URLs are dynamically created, it failed in some way.
