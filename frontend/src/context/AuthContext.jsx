/**
 * Authentication Context
 * Manages user authentication state throughout the application
 */
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [loginModalCallback, setLoginModalCallback] = useState(null);

  useEffect(() => {
    // Check if user is logged in on app start
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (error) {
        console.error('Error parsing saved user data:', error);
        localStorage.removeItem('user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  const openLoginModal = () => {
    if (loginModalCallback) {
      loginModalCallback();
    }
  };

  const registerLoginModalHandler = useCallback((callback) => {
    setLoginModalCallback(() => callback);
  }, []);

  const isAuthenticated = !!user;
  const isAdmin = user?.user_type === 'admin';

  const value = {
    user,
    isAuthenticated,
  isAdmin,
    isLoading,
    login,
    logout,
    openLoginModal,
    registerLoginModalHandler
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;