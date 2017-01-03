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
The first option is the switch between the crawl cli and the analyze cli:
- ```crawl``` crawls tweets from the (default: 100) most popular twitter users and stores them on disk.
- ```analyze``` analyzes social media status updates in order to determine, whether an account was compromised or not.

##### Crawling status updates
- ```-o /--output-path OUTPUT_PATH``` The output path of the generated dataset.
- ```--user-limit USER_LIMIT``` The maximum number of accounts to crawl.
- ```--limit LIMIT``` The maximum number of status updates per user to crawl. (default: 100)

##### Analyzing status updates
- ```-ut / --user-data-source USER_DATA_SOURCE``` The data source for tweets of the user that should be analyzed. Possible values are ```fth```, ```mp``` and ```twitter```.
- ```-uu / --user-twitter-id USER_TWITTER_ID``` The id of the twitter user, whose status updates should be analyzed.
- ```-up / --user-dataset-path USER_DATASET_PATH``` The path of the dataset of the user data source.
- ```-et / --ext-data-source EXT_DATA_SOURCE``` The data source for external tweets not written by the user. Possible values are ```fth```, ```mp``` and ```twitter```.
- ```-ep / --ext-dataset-path EXT_DATASET_PATH``` The path of the dataset of the external data source.
- ```-c / --classifier-type CLASSIFIER_TYPE``` The type of the classifier to be trained. Possible values are ```decision_tree``` and ```perceptron```.

#### Examples
```
# Crawl 50 most popular users
python cli.py -a crawl -o output.csv --user-limit 50

# Analyze twitter account of sebsatian_kliem against status updates from the 'Follow the Hashtag' dataset using the perceptron classifier
python cli.py analyze -ut twitter -uu sebastian_kliem -et fth -ep data/follow_the_hashtag_usa.csv -c perceptron
```

### Web App
```
# Run the app locally (DO NOT use this in production)
./run_app_dev.sh
```

The app takes a twitter url from a specific user as input and uses the perceptron classifier.
