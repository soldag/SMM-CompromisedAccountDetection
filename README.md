# CompromisedAccountDetection
This application was developed in the context of the [Social Media Mining seminar](https://hpi.de/studium/lehrveranstaltungen/it-systems-engineering/lehrveranstaltung/course/2016/wintersemester-20162017-social-media-mining.html) at Hasso-Plattner Institute. It aims to detect tweets in the timeline of a given user, which are suspicious in order to tell if the account was compromised.   

## Setup
### Docker
The app can be run using docker. The following steps are necessary:

1. Install docker. See https://www.docker.com/products/docker#/ for details.
2. Clone the repository.
3. Create the twitter API credentials file as described [below](#twitter-api-credentials).
4. Copy the twitter dataset into `data/tweets.csv`. It can be created using the CLI interface (see [CLI Reference](docs/cli.md)).
5. Go into the directory, build the image and run it.
```bash
cd /SMM-CompromisedAccountDetection
docker build -t smm-compromised-account-detection .
docker run -d -p 5000:5000 smm-compromised-account-detection
```

#### Mac
The app is available at `http://localhost:5000`.

#### Windows
Execute the following command to determine the IP of the `DOCKER_VM_IP`.
```bash
docker-machine ip default  # the machine could be named different from 'default' !
```

The app is available at `http://DOCKER_VM_IP:5000`.

### Native
#### Python
Python 3 is required to run the app.

#### Requirements
You have to install the required packages using ```pip``` and the necessary NLTK data packages:
```
pip install -r requirements.txt
python -m nltk.downloader punkt
```

### Twitter API credentials
For both options, you have to create a file `twitter_credentials.json` based on the template containing your Twitter API credentials. 

## Running
### Web App
The web app takes a twitter user id as input, crawls the tweets of the user and shows those, which are detected as suspicious.

For demo purposes the HTTP query parameter `demo=1` can be set to randomly insert some external tweets into the timeline of the user. These tweets should be detected by the app.

The app needs a dataset containing tweets that can be used as negative samples and for demo mode. It can be created by using our crawling command-line tool (see [CLI Reference](docs/cli.md)). 

```
# Starts the web app with default parameters.
python app.py
```

The app can be configured using the following command line arguments:

| Flag | Name           | Description                                                                                                              | Default         |
|------|----------------|--------------------------------------------------------------------------------------------------------------------------|-----------------|
| -H   | --data-source  | The hostname of the app.                                                                                                 | 0.0.0.0         |
| -P   | --dataset-path | The port for the app.                                                                                                    | 5000            |
| -s   | --data-source  | The data source for tweets that should be used for analyzing. Possible values are `fth`, `mp` and `twitter`.             | twitter         |
| -p   | --dataset-path | The path of the dataset that should be used for analyzing                                                                | data/tweets.csv |
| -c   | --classifier   | The classifier to be trained. Possible values are `decision_tree`, `one_class_svm`, `isolation_forest` and `perceptron`. | decision_tree   |


### Command Line Interface
The app provides a command line interface for crawling a dataset, tuning hyperparameters and evaluation. Have a look at the [CLI Reference](docs/cli.md).
