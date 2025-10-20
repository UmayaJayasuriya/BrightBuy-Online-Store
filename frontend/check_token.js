"""
Debug script to check your admin token
Run this in browser console while on your BrightBuy site:
"""

# Copy and paste this in your browser console (F12 -> Console tab):
"""
// Check if token exists
const token = localStorage.getItem('token');
console.log('Token exists:', !!token);

if (token) {
    // Decode the token (just the payload, not verifying signature)
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        
        const payload = JSON.parse(jsonPayload);
        console.log('Token payload:', payload);
        console.log('User type:', payload.user_type);
        console.log('User ID:', payload.sub);
        console.log('User name:', payload.user_name);
        
        // Check expiration
        const exp = new Date(payload.exp * 1000);
        const now = new Date();
        console.log('Token expires at:', exp);
        console.log('Current time:', now);
        console.log('Token expired?', now > exp);
        
        if (payload.user_type !== 'admin') {
            console.error('❌ You are NOT logged in as admin! User type:', payload.user_type);
        } else {
            console.log('✅ You are logged in as admin');
        }
        
        if (now > exp) {
            console.error('❌ Your token has EXPIRED! Please log in again.');
        } else {
            console.log('✅ Token is still valid');
        }
        
    } catch (e) {
        console.error('Error decoding token:', e);
    }
} else {
    console.error('❌ No token found! Please log in.');
}
"""
