#!/bin/bash
cd hamburg_website
scrapy crawl hamburg_events

cd ../meetup
scrapy crawl meetup_spider

cd ../eventbrite
scrapy crawl eventbrite_spider