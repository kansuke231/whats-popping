import React, { useState, useEffect } from 'react';
import './App.css';


function App() {
  const [events, setEvents] = useState([]);

  // Define dateStr outside useEffect so it's accessible in the component
  const today = new Date();
  const dateStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
  
  useEffect(() => {
     
      fetch(`http://127.0.0.1:5000/events/${dateStr}`)
          .then(response => response.json())
          .then(data => {
              setEvents(data);
          })
          .catch(error => {
              console.error("There was an error fetching the events", error);
          });
  }, []);


  return (
    
    <div className="App">
      <h1>What's popping in Hamburg today? ({dateStr})</h1>

      <table>
        <thead>
          <tr>
            <th>Event Image</th>
            <th>Title</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event, index) => (
            <tr key={index}>
              <td><img className="thumbnail" src={event.image} alt={event.title}/></td>
              <td><a href={event.link}>{event.title}</a></td>
              <td>{event.time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
