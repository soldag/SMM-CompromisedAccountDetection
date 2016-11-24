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
```python main.py [options]```

#### Options
- ```-p / --dataset-path FILE_PATH``` The path of the CSV dataset, which contains the posts. 
- ```-t / --dataset-type DATASET_TYPE``` The type of the specified dataset. (currently only ```fth```)
- ```-c / --classifier-type CLASSIFIER_TYPE``` The type of the classifier to be trained. (currently only ```decision_tree```)
