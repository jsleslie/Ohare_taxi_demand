# Predicting hourly taxi rides at Chicago's O'hare airport

Authors: Jarome Leslie, Derek Kruszewski

This project examines whether data on flight arrivals, seat counts, and passenger estimates may be combined with weather data to predict the hourly taxi demand.

**Chicago Taxi trips**

Taxi data for O'Hare International Airport ("ORD") was obtained from the City of Chicago by querying a Kaggle kernel of the dataset import from Google's BigQuery datawarehouse. The Kaggle kernel notebook may be accessed [here](https://www.kaggle.com/jleslie246/how-to-query-the-chicago-taxi-dataset?scriptVersionId=29149543). The dataset contains trips dating from 2013 to 2018 from approximately 7,000 licensed cabs in the city operated by private companies

The following code chunks describe how taxi data was extracted for the purposes of this project. First, the BigQuery tool `bq_helper` was imported following the directions provided in the [kaggle dataset documentation](https://www.kaggle.com/chicago/chicago-taxi-trips-bq).

```
import bq_helper
from bq_helper import BigQueryHelper
# https://www.kaggle.com/sohier/introduction-to-the-bq-helper-package
chicago_taxi = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="chicago_taxi_trips")
```
Next, SQL was used to select datetime parameters `YEAR`, `MONTH`, `DAY` and `HOUR` as well as the count of rides leaving the airport region. As seen in the Figure below, O'hare International Airport occupies its own city region block




```
 # ORD is located community area 76
query1 = """SELECT

pickup_community_area,
EXTRACT(YEAR FROM trip_start_timestamp) AS year,
EXTRACT(MONTH FROM trip_start_timestamp) AS month,
EXTRACT(DAY FROM trip_start_timestamp) AS day,
EXTRACT(HOUR FROM trip_start_timestamp) AS hour,
COUNT(1) AS rides

FROM
  `bigquery-public-data.chicago_taxi_trips.taxi_trips`
  
WHERE
    pickup_community_area = 76
    
GROUP BY
    pickup_community_area, year,month, day, hour

ORDER BY
    year,month, day, hour
    
        """
response1 = chicago_taxi.query_to_pandas_safe(query1, max_gb_scanned=10)                                  
response1.to_csv('ORD_outbound.csv')
```


**Weather data**

Weather data for O'Hare Internation Airport ("ORD") was obtained from the Iowa State University Iowa Environmental Mesonet ASOS Network accessed [here](https://mesonet.agron.iastate.edu/ASOS/)

**Flights data**
