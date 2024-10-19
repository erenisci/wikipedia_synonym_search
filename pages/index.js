// pages/index.js

import { useState } from 'react';

export default function Home() {
  const [word, setWord] = useState('');
  const [synonyms, setSynonyms] = useState([]);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    setError('');
    setSynonyms([]);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word }),
      });

      const data = await response.json();

      if (response.ok) {
        setSynonyms(data.synonyms);
      } else {
        setError(data.message);
      }
    } catch (error) {
      setError('Bir hata oluştu.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Wikipedia Eş Anlamlı Kelime Bulucu</h1>
      <input
        type="text"
        value={word}
        onChange={(e) => setWord(e.target.value)}
        placeholder="Kelime girin"
      />
      <button onClick={handleSearch}>Ara</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {synonyms.map((synonym, index) => (
          <li key={index}>
            {synonym.word} (Skor: {synonym.score.toFixed(2)})
          </li>
        ))}
      </ul>
    </div>
  );
}
