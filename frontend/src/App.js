import React, { useState, useEffect } from 'react';

function App() {
  const [value, setValue] = useState(null);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onmessage = (event) => {
      setValue(event.data);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div>
      <p>{value !== null ? `Valor atual: ${value}` : 'Carregando...'}</p>
    </div>
  );
}

export default App;
