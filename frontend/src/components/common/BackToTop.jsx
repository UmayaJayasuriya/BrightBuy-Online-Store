/**
 * BackToTop Component
 * Scroll to top button that appears when user scrolls down
 */
import React, { useState, useEffect } from 'react';
import './BackToTop.css';

const BackToTop = () => {
  const [isVisible, setIsVisible] = useState(false);

  // Show button when page is scrolled down
  useEffect(() => {
    const toggleVisibility = () => {
      if (window.pageYOffset > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', toggleVisibility);

    return () => {
      window.removeEventListener('scroll', toggleVisibility);
    };
  }, []);

  // Scroll to top smoothly
  const scrollToTop = (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  return (
    <>
      {isVisible && (
        <a
          href="#top"
          className="btn btn-primary btn-lg-square back-to-top"
          onClick={scrollToTop}
        >
          <i className="fa fa-arrow-up"></i>
        </a>
      )}
    </>
  );
};

export default BackToTop;
