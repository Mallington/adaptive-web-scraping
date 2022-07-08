# adaptive-web-scraping
![Pipeline](https://raw.githubusercontent.com/Mallington/adaptive-web-scraping/main/docs/diagrams/rcnn.jpg)

## Research into adapative web scraping
This is experimental software, developed as part of my dissertation research. My Dissertation was is called "API Second: An adaptive unstructured data extraction system". It involved the creation of a novel machine learning-based data extraction framework capable of learning to auto-navigate complex visual layouts, adapt to website updates over time, and to extract data from sites that it has never seen before, with a high degree of accuracy.

## Usage

This code is purely meant for research and is not at a stable point, I may choose to open source this project in future and make it more user friendly. If you're feeling adventurous, good luck: 

* Data can be generated using numerous manual and automatic methods by invoking: `manual_data_generator_runner.py`
* Two models need to be trained:
  * YoloV5 Object Recognition models
  * MLP Classifier Model (sk-Learn), can be adapted to use numerous other models in the sk-learn family
* Pipeline can be invoked using the AdaptivePredictor class:
```
predictor = AdaptivePredictor("YoloV5-Model.pt", "SK-Learn-Model.pkl")
predictor.predict_url(url, load_wait=10)
```
