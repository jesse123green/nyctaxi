# nyctaxi

Via is considering expanding its service – currently 6:30am to midnight. The main possibilities for expansion are weekends and late nights (midnight to 2am). We are trying to decide between these options and how to launch the option we choose, i.e. launch all at once, or limit to certain areas and/or customers. 

Using the NYC taxi data (described here: http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml, available either through BiqQuery https://bigquery.cloud.google.com/table/imjasonh-storage:nyctaxi.trip_data, or in smaller samples from http://www.andresmh.com/nyctaxitrips/), how would you answer the following questions:

Analysis questions:
1. Which of the expansion options is most beneficial and why?
	- total volume heatmap
	- per hour volume, M-Su [00-02)
	- per hour volume, M-Su [6-00)

	- People travelling in NYC have many different transportation options. Given Via's operational model and cost structure, high demand for pickups is the most important consideration.

	- Demand for taxis within the NYC Via operational area between 6am - Midnight on weekdays is on average ~20k passengers per hour (baseline). The demand for late night taxis during the week is only 42% of the baseline, while weekends 6am - Midnight and weeeknd late nights are 99% and 82% of the baseline respectively.

	- Weekend Expansion is the most beneficial, with more than double the demand of the late night option.

	- This simple demand-based analysis also assumes a well-balanced distribution of pickup and dropoff locations.

2. If we were to launch weekend service, should we alter our hours of operation or keep 6:30am to midnight? Why?
	- The hours should be altered to Sa-Su 10am - Midnight and Fri - Sat late night. 

	- Pushing the operational start time on the weekend increases the volume to 96% of the baseline.

3. Would you launch the expansion in our entire area of service or just for certain areas? If only certain areas, which ones and why?

4. We currently offer a flat fee of $5 per ride anywhere before 9pm, and $7.95 after 9pm. Is this still reasonable for your proposed expansion? If not, how much should we charge? Why?