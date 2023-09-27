#!/bin/bash
cd hamburg_website
scrapy crawl hamburg_events

cd ../meetup
scrapy crawl hamburg_meetup

cd ../eventbrite
scrapy crawl eventbrite