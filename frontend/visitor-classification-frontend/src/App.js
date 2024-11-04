import React, { useState } from 'react';
import Questionnaire from './components/Questionnaire';
import axios from 'axios';

const App = () => {
  const [url, setUrl] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/scrape-and-classify', { url });
      setData(response.data);
    } catch (err) {
      setError(err.response && err.response.data ? err.response.data.error : 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Visitor Classification</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={handleUrlChange}
          placeholder="Enter URL to scrape"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Classify'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {data && <Questionnaire data={data} />}
    </div>
  );
};

export default App;
