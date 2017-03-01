# SMM-CompromisedAccountDetection

## Setup
#### Python
Python 3 is required to run the app.

#### Python packages
You have to install the required packages using ```pip```:
```
pip install -r requirements.txt
```

#### NLTK Data
The application additionally needs the following NLTK data packages:
- ```punkt``` - Punkt Tokenizer Models

For installation instructions please visit [http://www.nltk.org/data.html](http://www.nltk.org/data.html).

#### Twitter API credentials
You have to create a file `twitter_credentials.json` based on the template containing your Twitter API credentials. 

## Usage
### Command Line Interface
```python cli.py [options]```

#### Options
##### General arguments
The first option is the switch between the crawl cli, the analyze cli, and the evaluate cli:
- ```crawl``` crawls tweets from the (default: 100) most popular twitter users (people with the most followers) and stores them on disk.
- ```analyze``` determines the best suited hyper-parameter combinations for a certain classifier based on a given data set.
- ```evaluate``` evaluates the anomaly detection approach using cross-validation.

##### Crawling status updates
- ```-o /--output-path OUTPUT_PATH``` The output path of the generated dataset.
- ```--user-limit USER_LIMIT``` The maximum number of accounts to crawl. (default: 100)
- ```--limit LIMIT``` The maximum number of tweets per account to crawl. (default: 0)

##### Analyzing classifier
- ```-t / --data-source DATA_SOURCE``` The data source for tweets that should be used for classifier analysis. Possible values are ```fth```, ```mp``` and ```twitter```.
- ```-p / --dataset-path DATASET_PATH``` The path of the dataset that should be used for classifier analysis.
- ```-c / --classifier-type CLASSIFIER_TYPE``` The type of the classifier to be analyzed. Possible values are ```decision_tree``` and ```perceptron```.

The report of the analysis is written to disk (```./classifier_optimization_report.log```).

##### Evaluation
- ```-t / --data-source DATA_SOURCE``` The data source for tweets that should be used for cross-validation. Possible values are ```fth```, ```mp``` and ```twitter```.
- ```-p / --dataset-path DATASET_PATH``` The path of the dataset that should be used for cross-validation.
- ```-c / --classifier-type CLASSIFIER_TYPE``` The type of the classifier to be trained. Possible values are ```decision_tree```, ```one_class_svm```, ```isolation_forest``` and ```perceptron```.
- ```--evaluation-rounds"```  Number of rounds the evaluation is executed (default: 10). Reduces the variation caused by sampling.
- ```--no-scaling``` Disable feature scaling.

#### Examples
```
# Crawl the 50 most popular users' tweets
python cli.py crawl -o twitter_data.csv --user-limit 50

# Analyze the hyper-parameter combinations for  the Decision Tree classifier on the crawled twitter dataset
python cli.py analyze -t twitter -c decision_tree -p twitter_data.csv

# Evaluate the performance of the Decision Tree classifier on the crawled twitter dataset
python cli.py evaluate -t twitter -c decision_tree -p twitter_data.csv
```

### Web App
```
# Start the app
python app.py

# DEBUG mode (DO NOT use this in production)
./run_app_dev.sh
```

The app runs on port 5000. It takes a twitter user id as input and uses the decision tree classifier. By setting query parameter `demo=1`, some external tweets are inserted randomly into the timeline of the user. These tweets should be detected by the app.
