import React, { useState, useEffect } from 'react';

function App() {
  const [value, setValue] = useState(null);

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetch('http://localhost:8000/mensagem')
        .then(response => {
          if (!response.ok) {
            throw new Error('Deu ruim!');
          }
          return response.json();
        })
        .then(data => {
          console.log(data);
          setValue(data.mensagem);
        })
        .catch(error => {
          console.log(error);
        });
    }, 1000);

    return () => {
      clearInterval(intervalId);
    };
  }, []);

  return (
    <div>
      <h1>{value !== null ? `Valor atual: ${value}` : 'Carregando...'}</h1>
    </div>
  );
}

export default App;
