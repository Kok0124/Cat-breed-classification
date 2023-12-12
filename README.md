# Cat-breed-classification

This repo is an image classification demo using machine learning. It can be used to classify cats by their breeds. The dataset that I used for this project can be found [here](https://www.kaggle.com/datasets/shawngano/gano-cat-breed-image-collection). I created three different models of which two were made by me and one using a pre-trained model.

The best way to run these is to import them in a Google Colab enviroment. **Do not forget to add your own Kaggle API file.**

## Basic model 1

This is a badly structured deep neural network that has lots of parameters but achieved bad results. It functions as a bad example in this repo.

## Basic model 2

In this model, I used convolutional max pool layers alternately. The parameter number is acceptable and I achieved better results than with the first one. It probably would have scored better with more epochs and some fine-tuning.

## Transfer learning model

In this solution, I used the Inception model by Google, which is a pre-trained model for image recognition. I froze the model layers and added some additional layers. I achieved the best results with this approach.
