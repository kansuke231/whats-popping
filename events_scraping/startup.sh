#!/bin/bash
cd hamburg_website
scrapy crawl hamburg_events

cities=("hamburg" "münchen")

cd ../meetup
for city in "${cities[@]}"
do
   echo "Scraping for $city"
   scrapy crawl meetup -a city=$city
done


cd ../eventbrite
for city in "${cities[@]}"
do
   echo "Scraping for $city"
   scrapy crawl eventbrite -a city=$city
done
