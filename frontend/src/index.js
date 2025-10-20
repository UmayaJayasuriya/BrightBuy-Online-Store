/**
 * Main entry point for the React application
 * Renders the App component into the root DOM element
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/mermaid-garnet-symphony.css';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
