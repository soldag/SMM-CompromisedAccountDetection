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
##### Required arguments
- ```-t / --provider-type DATA_PROVIDER_TYPE``` The type of the specified data provider, which supplies the status updates.
- ```-c / --classifier-type CLASSIFIER_TYPE``` The type of the classifier to be trained. (currently only ```decision_tree```)

##### Data provider dependent arguments
###### File-based data providers (```fth``` or ```mp```)
- ```--dataset-path FILE_PATH``` The path of the CSV dataset, which contains the status updates. 

###### Twitter provider (```twitter```)
- ```--twitter-user TWITTER_USER_ID``` The id of the twitter user, whose status updates should be analyzed.

###### Optional arguments
- ```-n / --experiments-count NUMBER_OF_EXPERIMENTS``` The number of experiments to run. (default: 10)

### Web App
```./run_app_dev.sh```
