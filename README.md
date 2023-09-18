# Compiled masshooting data for analysis and ml

Data collected from gunviolence.org and [datausa](https://datausa.io)

This is compiled 3 years ago before college, so a lot of mistakes. The neural network I was using back then did not like the data, but I think I was just bad.

## Future Plan

Will retrain on different models and try different cleaning methods as well. I spent way too long compiling this data back in the day to just leave it.

## Methods

Created a web scraper to retrieve data from datusa to give more context to the location data of each gun violence incident.

I did not mask the user agent, so my ip kept getting blocked when doing more in depth searches. Had to settle for their own api and then parse the json.

The included data_scrapper.py file is not inclusive, I being dumb deleted methods that I found to be close enough to repeated.

### Normalization

I did not know at the time that there are built in methods to normalize dataframes, so I did it all manually. 