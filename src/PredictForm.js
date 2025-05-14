
import React, { useState } from 'react';
import axios from 'axios';

function PredictForm() {
  const [rainfall, setRainfall] = useState('');
  const [pesticides, setPesticides] = useState('');
  const [temperature, setTemperature] = useState('');
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:5000/predict', {
        rainfall: parseFloat(rainfall),
        pesticides: parseFloat(pesticides),
        temperature: parseFloat(temperature)
      });
      setPrediction(res.data.predicted_yield);
    } catch (err) {
      alert('Error predicting: ' + err.message);
    }
  };

  return (
    <div className="card">
      <h2>Single Prediction</h2>
      <form onSubmit={handleSubmit}>
        <input type="number" step="any" placeholder="Rainfall (mm)" value={rainfall} onChange={(e) => setRainfall(e.target.value)} required />
        <input type="number" step="any" placeholder="Pesticides (tonnes)" value={pesticides} onChange={(e) => setPesticides(e.target.value)} required />
        <input type="number" step="any" placeholder="Temperature (°C)" value={temperature} onChange={(e) => setTemperature(e.target.value)} required />
        <button type="submit">Predict</button>
      </form>
      {prediction !== null && <p>🌱 Predicted Yield: <strong>{prediction}</strong> hg/ha</p>}
    </div>
  );
}

export default PredictForm;
