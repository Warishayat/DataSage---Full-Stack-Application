import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import axios from 'axios';
import { Mail, Lock, LogIn, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const { login } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(
      'https://datasage-backend-jrjo.onrender.com/auth/login',
      formData,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

      login(response.data.access_token, response.data.user);
      
      toast.success("Welcome back to DataSage!");
      navigate('/chat-csv'); 
    } catch (err) {
      const errorMsg = err.response?.data?.detail || "Invalid Email or Password";
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4 py-12 bg-slate-950">
      <div className="w-full max-w-md bg-white/5 border border-white/10 backdrop-blur-xl p-8 rounded-3xl shadow-2xl relative overflow-hidden">
        {/* Subtle Decorative Glow */}
        <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/10 blur-3xl rounded-full -mr-10 -mt-10" />

        <div className="text-center mb-10 relative z-10">
          <h2 className="text-3xl font-bold text-white tracking-tight">Welcome Back</h2>
          <p className="text-gray-400 mt-2 text-sm">The Data Sage is waiting for your input</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6 relative z-10 text-white">
          <div className="relative group">
            <Mail className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-cyan-400 transition-colors" size={20} />
            <input 
              type="email" 
              placeholder="Email Address"
              className="w-full bg-slate-900/50 border border-white/10 rounded-xl py-3 pl-11 pr-4 focus:outline-none focus:border-cyan-500 transition-all placeholder:text-gray-600"
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
              disabled={loading}
            />
          </div>

          <div className="relative group">
            <Lock className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-cyan-400 transition-colors" size={20} />
            <input 
              type="password" 
              placeholder="Password"
              className="w-full bg-slate-900/50 border border-white/10 rounded-xl py-3 pl-11 pr-4 focus:outline-none focus:border-cyan-500 transition-all placeholder:text-gray-600"
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
              disabled={loading}
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className={`w-full font-bold py-3 rounded-xl transition-all flex items-center justify-center group ${
              loading 
                ? 'bg-cyan-900 cursor-not-allowed opacity-70' 
                : 'bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-90 text-slate-950 shadow-lg shadow-cyan-500/20'
            }`}
          >
            {loading ? (
              <Loader2 className="animate-spin mr-2" size={20} />
            ) : (
              <>
                Sign In
                <LogIn className="ml-2 group-hover:translate-x-1 transition-transform" size={18} />
              </>
            )}
          </button>
        </form>

        <p className="text-center text-gray-400 mt-8 text-sm relative z-10">
          Don't have an account? <Link to="/register" className="text-cyan-400 hover:underline hover:text-cyan-300 transition-colors">Sign up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;