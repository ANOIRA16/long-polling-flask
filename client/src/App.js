import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [update, setUpdate] = useState('');

  const pollServer = () => {
    fetch('http://localhost:5000/update/poll')
    .then(response => response.json())
    .then(data => {
      if (data.hasUpdate) {
        console.log(`Update received: ${data.message}`);
        setUpdate(data.message); 
      }
    })
    .catch(error => console.error('Polling error:', error));
  };

  useEffect(() => {
    const interval = setInterval(pollServer, 180000); 
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h2>Server Update</h2>
        <p>{update || "Waiting for updates..."}</p>
      </header>
    </div>
  );
}

export default App;
