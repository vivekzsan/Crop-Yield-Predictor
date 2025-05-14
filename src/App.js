
import React from 'react';
import PredictForm from './PredictForm';
import BatchUpload from './BatchUpload';

function App() {
  return (
    <div className="app">
      <h1>Crop Yield Predictor</h1>
      <PredictForm />
      <BatchUpload />
    </div>
  );
}

export default App;
