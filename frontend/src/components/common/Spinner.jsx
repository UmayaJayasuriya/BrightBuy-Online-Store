/**
 * Spinner Component
 * Loading spinner displayed during initial page load
 */
import React, { useState, useEffect } from 'react';
import './Spinner.css';

const Spinner = () => {
  const [show, setShow] = useState(true);

  useEffect(() => {
    // Hide spinner after a brief delay
    const timer = setTimeout(() => {
      setShow(false);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  if (!show) return null;

  return (
    <div
      id="spinner"
      className="show bg-white position-fixed translate-middle w-100 vh-100 top-50 start-50 d-flex align-items-center justify-content-center"
    >
      <div
        className="spinner-border text-primary"
        style={{ width: '3rem', height: '3rem' }}
        role="status"
      >
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );
};

export default Spinner;
