import React, { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    // Handle login logic here
    console.log('Login clicked');
  };

  const handleSignUp = () => {
    // Navigate to the sign-up page or handle sign-up logic
    console.log('Sign-Up clicked');
    navigate('/signup'); // Example navigation to sign-up page
  };

  const handleForgotPassword = () => {
    // Handle forgot password logic
    console.log('Forgot password clicked');
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="button" onClick={handleLogin}>Login</button>
        <button
          type="button"
          className="forgot-password-button"
          onClick={handleForgotPassword}
        >
          Forgot password?
        </button>
        <button
          type="button"
          className="sign-up-button"
          onClick={handleSignUp}
        >
          Sign Up
        </button>
      </div>
    </div>
  );
};

export default Login;
