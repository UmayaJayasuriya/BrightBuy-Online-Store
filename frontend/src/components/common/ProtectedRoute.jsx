/**
 * Protected Route Component
 * Protects admin routes and redirects non-admin users
 */
import React from 'react';
import { Navigate } from 'react-router-dom';
// Adjusted path: this file is in components/common, context is at src/context
import { useAuth } from '../../context/AuthContext';

const ProtectedRoute = ({ children, requireAdmin = false, requireSuperAdmin = false }) => {
  const { isAuthenticated, hasAdminPrivileges, isSuperAdmin, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-container" style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '50vh' 
      }}>
        <div className="spinner" style={{
          border: '4px solid #f3f3f3',
          borderTop: '4px solid #667eea',
          borderRadius: '50%',
          width: '50px',
          height: '50px',
          animation: 'spin 1s linear infinite'
        }}></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  if (requireSuperAdmin && !isSuperAdmin) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '3rem',
        background: 'white',
        borderRadius: '10px',
        margin: '2rem',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
      }}>
        <h2 style={{ color: '#dc3545' }}>Access Denied</h2>
        <p>You need super admin privileges to access this page.</p>
      </div>
    );
  }

  if (requireAdmin && !hasAdminPrivileges) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '3rem',
        background: 'white',
        borderRadius: '10px',
        margin: '2rem',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
      }}>
        <h2 style={{ color: '#dc3545' }}>Access Denied</h2>
        <p>You need admin privileges to access this page.</p>
      </div>
    );
  }

  return children;
};

export default ProtectedRoute;