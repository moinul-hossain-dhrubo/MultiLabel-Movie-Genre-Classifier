# MULTILABEL-MOVIE-GENRE-CLASSIFIER (Project In Progress)

## Objective
The goal of this project was to build a multi-label text classification model that can predict movie genres from its description. The project includes data collection, cleaning, model training, deployment, and API integration. <br/>
The model can classify 21 different types of book genres <br/>The keys of `deployment\genre_types_encoded.json` shows the book genres

 ## Data Collection

Data was collected from IMDB official Website Listing: https://www.imdb.com/search/title/?title_type=feature <br/>

**Movie Details Scraping:** movie title, description and genres are scraped with `scraper\scrape.py` and they are stored in `data\movie_data.csv`

In total, 13,001 movie details were scraped

## Data Preprocessing

Initially, duplicates and missing values were dropped. After that, two of the 23 genres(Film and Noir) were dropped as those genres are rare and training with them could potentially drop the accuracy of the model. The preprocessing can be found in `notebooks/Project_NLP.ipynb`. The cleaned dataset can be found in `data` folder

## Model Training

Finetuned a `distilrobera-base` model from HuggingFace Transformers using Fastai and Blurr. The model training notebook can be found in `notebooks/Project_NLP.ipynb`

## Model Compression and ONNX Inference

The trained model has a memory of 300+MB. I compressed this model using ONNX quantization and brought it under 80MB. The model can be found in `models` folder.

## Model Deployment

The compressed model is deployed to HuggingFace Spaces Gradio App. The implementation can be found in `deployment` folder.


## Web Deployment
Deployed a Flask App built to take descprition and show the genres as output. Check `flask ` branch. The website is live [here](https://multilabel-movie-genre-classifier.onrender.com/) 
