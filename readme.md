# eInk Twitter Viewer

This is a small Python application which displays tweets on an eInk display connected to a Raspberry Pi. It is designed to run on the Waveshare 2.13" display which is available as a pHAT and is almost exactly the same size as the Pi Zero.

The application fetches local Twitter trends and displays the top tweets for each trend.

## Setup

This application uses the Twitter API so you'll need a set of API Keys and Access Token in order to run it.

The application expects the following environment variables containing the Twitter API credentials:

|Environment Variable Name     |Description                  |
|------------------------------|-----------------------------|
|`TWITTER_CONSUMER_KEY`        |Twitter API key              |
|`TWITTER_CONSUMER_SECRET`     |Twitter API secret key       |
|`TWITTER_ACCESS_TOKEN_KEY`    |Twitter access token         |
|`TWITTER_ACCESS_TOKEN_SECRET` |Twiter access token secret   |


## Running

`python -m twitter_trends` to run in test mode. This will output a file containing an image of what would be displayed on the eInk screen.

`python -m twitter_trends -epaper` to run in epaper mode on the Raspberry Pi with an attached eInk display.

## Demo

The video below demonstrates the code running on a Raspberry PI Zero W. This video is running at 5x normal speed.

[![Demo Video](https://img.youtube.com/vi/UFxe9dI1njk/0.jpg)](https://youtu.be/UFxe9dI1njk "Demo Video")