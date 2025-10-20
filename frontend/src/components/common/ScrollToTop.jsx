/**
 * ScrollToTop Component
 * Automatically scrolls to the top of the page when the route changes
 * This improves UX by ensuring users always see the top of a new page
 */
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    // Scroll to top whenever pathname changes
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'instant' // Use 'smooth' for animated scroll, 'instant' for immediate
    });
  }, [pathname]);

  return null; // This component doesn't render anything
}

export default ScrollToTop;
