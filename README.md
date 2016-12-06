# SMM-CompromisedAccountDetection

## Setup
#### Python packages
You have to install the required packages using ```pip```:
```
pip install -r requirements.txt
```

#### NLTK Data
The application additionally needs the following NLTK data packages:
- ```punkt``` - Punkt Tokenizer Models

For installation instructions please visit [http://www.nltk.org/data.html](http://www.nltk.org/data.html).

## Usage
### Command Line Interface
```python cli.py [options]```

#### Options
##### General arguments
- ```-a / --action ACTION``` The action that should be performed. Possible values are `crawl` and `analyze`
- ```-t / --data-source-type DATA_SOURCE_TYPE``` The type of the specified data source, which contains the status updates.

##### Crawling status updates
- ```-p / --dataset-path FILE_PATH``` The path of the output dataset, that should contain the crawled status updates. 
- ```--user-limit LIMIT``` The maximum number of accounts to crawl. (default: 100)

##### Analyzing status updates
- ```-c / --classifier-type CLASSIFIER_TYPE``` The type of the classifier to be trained. (currently only ```decision_tree```)
- ```-p / --dataset-path FILE_PATH``` The path of the dataset, which contains the status updates. 
- ```-u / --twitter-user TWITTER_USER_ID``` The id of the twitter user, whose status updates should be analyzed.
- ```-n / --experiments-count NUMBER_OF_EXPERIMENTS``` The number of experiments to run. (default: 10)

#### Examples
```
# Crawl 50 most popular users
python cli.py -a crawl -t twitter -p output.csv --user-limit 50

# Analyze 'Follow the Hashtag' dataset using an decision tree
python cli.py -a analyze -t fth -p fth.csv -c decision_tree

# Analyze twitter user @katyperry using an decision tree with 150 experiments
python cli.py -a analyze -t twitter -u katyperry -c decision_tree -n 150
```

### Web App
```
./run_app_dev.sh
```
