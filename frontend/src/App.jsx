/**
 * Main App Component
 * Sets up routing and global context providers for the entire application
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CartProvider } from './context/CartContext';
import { AuthProvider } from './context/AuthContext';
import './App.css';

// Import CSS
import 'bootstrap/dist/css/bootstrap.min.css';
import './theme.css'; // New theme colors
import './assets/css/style.css';

// Layout Components
import Header from './components/layout/Header';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// Page Components
import Home from './pages/Home';
import Shop from './pages/Shop';
import Single from './pages/Single';
import Bestseller from './pages/Bestseller';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import Payment from './pages/Payment';
import Profile from './pages/Profile';
import Contact from './pages/Contact';
import Admin from './pages/Admin';
import Favorites from './pages/Favorites';

// Common Components
import Spinner from './components/common/Spinner';
import BackToTop from './components/common/BackToTop';
import ScrollToTop from './components/common/ScrollToTop';

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <div className="App">
            <ScrollToTop />
            <Spinner />
            <Header />
            <Navbar />
          
          <div className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/shop" element={<Shop />} />
              <Route path="/single/:id" element={<Single />} />
              <Route path="/bestseller" element={<Bestseller />} />
              <Route path="/cart" element={<Cart />} />
              <Route path="/checkout" element={<Checkout />} />
              <Route path="/payment" element={<Payment />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/favorites" element={<Favorites />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/admin" element={<Admin />} />
            </Routes>
          </div>

          <Footer />
          <BackToTop />
        </div>
      </Router>
    </CartProvider>
    </AuthProvider>
  );
}

export default App;
