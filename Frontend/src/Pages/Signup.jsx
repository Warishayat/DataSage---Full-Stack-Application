import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import axios from 'axios';
import { User, Mail, Lock, ArrowRight, Loader2 } from 'lucide-react';

const Signup = () => {
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('https://datasage-backend-jrjo.onrender.com/auth/register', formData);
      toast.success(response.data.message || "Registration Successful!");
      navigate('/login');
    } catch (err) {
      toast.error(err.response?.data?.detail || "Registration Failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4 py-12 bg-slate-950">
      <div className="w-full max-w-md bg-white/5 border border-white/10 backdrop-blur-xl p-8 rounded-3xl shadow-2xl">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-white">Join DataSage</h2>
          <p className="text-gray-400 mt-2 text-sm">Start turning data into wisdom</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 text-white">
          <div className="relative group">
            <User className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-emerald-400 transition-colors" size={20} />
            <input 
              type="text" 
              placeholder="Full Name"
              className="w-full bg-slate-900/50 border border-white/10 rounded-xl py-3 pl-11 pr-4 focus:outline-none focus:border-emerald-500 transition-all placeholder:text-gray-600"
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
            />
          </div>

          <div className="relative group">
            <Mail className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-emerald-400 transition-colors" size={20} />
            <input 
              type="email" 
              placeholder="Email Address"
              className="w-full bg-slate-900/50 border border-white/10 rounded-xl py-3 pl-11 pr-4 focus:outline-none focus:border-emerald-500 transition-all placeholder:text-gray-600"
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>

          <div className="relative group">
            <Lock className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-emerald-400 transition-colors" size={20} />
            <input 
              type="password" 
              placeholder="Password"
              className="w-full bg-slate-900/50 border border-white/10 rounded-xl py-3 pl-11 pr-4 focus:outline-none focus:border-emerald-500 transition-all placeholder:text-gray-600"
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              required
            />
          </div>

          <button 
            type="submit" 
            disabled={loading} 
            className={`w-full font-bold py-3 rounded-xl transition-all flex items-center justify-center group ${
              loading ? 'bg-emerald-800 cursor-not-allowed opacity-70' : 'bg-emerald-500 hover:bg-emerald-600 text-slate-950 shadow-lg shadow-emerald-500/20'
            }`}
          >
            {loading ? (
              <Loader2 className="animate-spin mr-2" size={20} />
            ) : (
              <>
                Create Account
                <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={18} />
              </>
            )}
          </button>
        </form>

        <p className="text-center text-gray-400 mt-8 text-sm">
          Already have an account? <Link to="/login" className="text-emerald-400 hover:underline">Log in</Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;