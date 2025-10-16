/**
 * Authentication Context
 * Manages user authentication state throughout the application
 */
import React, { createContext, useContext, useState, useEffect } from 'react';

// Backend API base URL (configurable via env)
const API_BASE = process.env.REACT_APP_API_URL || '';

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
  const [token, setToken] = useState(null);

  useEffect(() => {
    // Check if user is logged in on app start
    const savedUser = localStorage.getItem('user');
    const savedToken = localStorage.getItem('token');
    
    if (savedUser && savedToken) {
      try {
        setUser(JSON.parse(savedUser));
        setToken(savedToken);
      } catch (error) {
        console.error('Error parsing saved user data:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
    setIsLoading(false);
  }, []);

  const login = (userData, accessToken) => {
    const userWithAdminInfo = {
      ...userData,
      is_admin: userData.is_admin || false,
      user_type: userData.user_type || 'customer'
    };
    
    setUser(userWithAdminInfo);
    setToken(accessToken);
    localStorage.setItem('user', JSON.stringify(userWithAdminInfo));
    localStorage.setItem('token', accessToken);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  };

  const openLoginModal = () => {
    if (loginModalCallback) {
      loginModalCallback();
    }
  };

  const registerLoginModalHandler = (callback) => {
    setLoginModalCallback(() => callback);
  };

  // Authentication helpers
  const isAuthenticated = !!user && !!token;
  const isAdmin = user?.is_admin || false;
  const isSuperAdmin = user?.user_type === 'admin';
  const isManager = user?.user_type === 'manager';
  const hasAdminPrivileges = isAdmin || isSuperAdmin || isManager;

  // API helper function to make authenticated requests
  const makeAuthenticatedRequest = async (url, options = {}) => {
    if (!token) {
      throw new Error('No authentication token available');
    }

    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    };

    const requestOptions = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const finalUrl = /^https?:\/\//i.test(url) ? url : `${API_BASE}${url}`;
      const response = await fetch(finalUrl, requestOptions);
      
      if (response.status === 401) {
        // Token expired or invalid, logout user
        logout();
        throw new Error('Authentication expired, please login again');
      }
      
      return response;
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  };

  const value = React.useMemo(() => ({
    user,
    token,
    isAuthenticated,
    isAdmin,
    isSuperAdmin,
    isManager,
    hasAdminPrivileges,
    isLoading,
    login,
    logout,
    openLoginModal,
    registerLoginModalHandler,
    makeAuthenticatedRequest
  }), [user, token, isAuthenticated, isAdmin, isSuperAdmin, isManager, hasAdminPrivileges, isLoading]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;