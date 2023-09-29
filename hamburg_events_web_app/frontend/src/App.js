import React, { useState, useEffect } from 'react';
import './AppOutput.css';

import {Card, CardHeader, CardBody, Image} from "@nextui-org/react";
import { NextUIProvider } from '@nextui-org/react';

function App() {
  const [events, setEvents] = useState([]);

  const BACKEND_URL =  process.env.REACT_APP_BACKEND_URL|| 'http://127.0.0.1:5000';

  // Define dateStr outside useEffect so it's accessible in the component
  const today = new Date();
  const dateStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
  
  useEffect(() => {
     
      fetch(`${BACKEND_URL}/events/${dateStr}`)
          .then(response => response.json())
          .then(data => {
              setEvents(data);
          })
          .catch(error => {
              console.error("There was an error fetching the events", error);
          });
  }, []);


  return (
    <NextUIProvider>
      <div className="App">
        <h1>What's popping in Hamburg today? ({dateStr})</h1>
    
        <div className="cards-container">
          {events.map((event, index) => (
            <Card key={index} className="event-card py-4">
              <CardHeader className="pb-0 pt-2 px-4 flex-col items-start">
                <h4 className="font-bold text-large">
                  <a href={event.link}>{event.title}</a>
                </h4>
                <small className="text-default-500">{event.time}</small>
              </CardHeader>
              <CardBody className="overflow-visible py-2">
                <Image
                  alt="Card background"
                  className="object-cover rounded-xl"
                  src={event.image}
                  width={270}
                />
              </CardBody>
            </Card>
          ))}
        </div>
      </div>
    </NextUIProvider>
  );
  
}

export default App;
