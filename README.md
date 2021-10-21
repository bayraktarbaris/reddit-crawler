# reddit-crawler

## Installation:

pip install -r requirements.txt

## Run
For writing Parquet files:\
```bin/write```

Files are located in:

For reading Parquet files:\
```bin/write```

## Data Types
### Submission:

| Field           | Type    |
|-----------------|---------|
| title           | string  |
| selftext        | string  |
| id              | string  |
| upvote_ratio    | float   |
| num_comments    | integer |
| link_flair_text | string  |
| score           | integer |
| created_utc     | long    |
| author          | string  |
| author_fullname | string  |
| retrieved_on    | long    |

### Comment:

| Field            | Type    |
|------------------|---------|
| body:            | string  |
| id:              | string  |
| score:           | integer |
| author:          | string  |
| author_fullname: | string  |
| parent_id:       | string  |
| created_utc:     | long    |
