# Command Line Interface
## Usage
```python cli.py [option] [arguments]```

## Options
### crawl
Crawls tweets from the most popular twitter users (people with the most followers) and stores them on disk. The list of twitter users is stored in [popular_twitter_users.csv](../crawler/popular_twitter_users.csv).

| Flag | Name          | Description                                        | Default      |
|------|---------------|----------------------------------------------------|--------------|
| -o   | --output-path | The output path of the crawled dataset.            |              |
|      | --user-limit  | The maximum number of accounts to crawl.           | 100          |
|      | --limit       | The maximum number of tweets per account to crawl. | 0 (no limit) |

### tune
Determines the best suited hyper-parameter combinations for a certain classifier based on a given data set. Only supported for Perceptron and Decision Tree.

| Flag | Name           | Description                                                                                                            | Default |
|------|----------------|------------------------------------------------------------------------------------------------------------------------|---------|
| -s   | --data-source  | The data source for tweets that should be used for classifier analysis. Possible values are `fth`, `mp` and `twitter`. |         |
| -p   | --dataset-path | The path of the dataset that should be used for classifier analysis.                                                   |         |
| -c   | --classifier   | The classifier to be analyzed. Possible values are `decision_tree` and `perceptron`.                                   |         |

The report of the analysis is written to disk (```./classifier_optimization_report.log```).

### evaluate
Evaluates the anomaly detection approach using cross-validation. 

| Flag | Name                | Description                                                                                                              | Default         |
|------|---------------------|--------------------------------------------------------------------------------------------------------------------------|-----------------|
| -s   | --data-source       | The data source for tweets that should be used for cross-validation. Possible values are `fth`, `mp` and `twitter`.      |                 |
| -p   | --dataset-path      | The path of the dataset that should be used for cross-validation.                                                        |                 |
| -c   | --classifier        | The classifier to be trained. Possible values are `decision_tree`, `one_class_svm`, `isolation_forest` and `perceptron`. |                 |
|      | --evaluation-rounds | Number of rounds the evaluation is executed. Reduces the variation caused by sampling.                                   | 10              |
|      | --no-scaling        | Disables feature scaling.                                                                                                | True            |
| -o   | --output-path       | The path of the file the results should be written to.                                                                   | evaluation.xlsx | 

## Examples
```
# Crawl the 50 most popular users' tweets
python cli.py crawl -o twitter_data.csv --user-limit 50

# Analyze the hyper-parameter combinations for  the Decision Tree classifier on the crawled twitter dataset
python cli.py tune -s twitter -c decision_tree -p twitter_data.csv

# Evaluate the performance of the Decision Tree classifier on the crawled twitter dataset
python cli.py evaluate -s twitter -c decision_tree -p twitter_data.csv
```
