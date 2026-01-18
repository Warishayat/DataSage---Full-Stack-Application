import React, { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { Menu, X, Database, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';

const Navbar = () => {
  const { isLoggedIn, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogoutAction = () => {
    logout();
    toast.info("Logged out successfully");
    navigate('/login');
    setIsOpen(false);
  };

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Chat CSV', path: '/chat-csv' },
    { name: 'Insights', path: '/insights' },
    { name: 'Contact', path: '/contact' },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-white/10 text-white font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <Database className="w-8 h-8 text-emerald-500 group-hover:rotate-12 transition-transform" />
            <span className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              DataSage
            </span>
          </Link>

          {/* Desktop Links */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <NavLink
                key={link.name}
                to={link.path}
                className={({ isActive }) =>
                  `text-sm font-medium transition-colors hover:text-emerald-400 ${
                    isActive ? 'text-emerald-400 font-bold underline underline-offset-4' : 'text-gray-300'
                  }`
                }
              >
                {link.name}
              </NavLink>
            ))}

            <div className="flex items-center space-x-4 border-l border-white/20 pl-6">
              {isLoggedIn ? (
                <button 
                  onClick={handleLogoutAction}
                  className="flex items-center space-x-2 px-4 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg transition-all border border-red-500/20 text-sm font-bold"
                >
                  <LogOut size={18} />
                  <span>Logout</span>
                </button>
              ) : (
                <>
                  <Link to="/login" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">Login</Link>
                  <Link to="/register" className="px-5 py-2 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold rounded-full text-sm transition-all shadow-lg shadow-emerald-500/20">
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button onClick={() => setIsOpen(!isOpen)} className="p-2 text-gray-400 hover:text-white transition-colors focus:outline-none">
              {isOpen ? <X size={28} /> : <Menu size={28} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {isOpen && (
        <div className="md:hidden bg-slate-900 border-b border-white/10 p-4 space-y-4 animate-in slide-in-from-top duration-300">
          {navLinks.map((link) => (
            <Link key={link.name} to={link.path} onClick={() => setIsOpen(false)} className="block text-gray-300 hover:text-emerald-400 py-2 transition-colors">
              {link.name}
            </Link>
          ))}
          <hr className="border-white/10" />
          {isLoggedIn ? (
            <button onClick={handleLogoutAction} className="w-full text-left py-2 text-red-400 flex items-center space-x-2 font-bold transition-all">
              <LogOut size={18} /> <span>Logout</span>
            </button>
          ) : (
            <div className="flex flex-col space-y-4 pt-2">
              <Link to="/login" onClick={() => setIsOpen(false)} className="text-gray-300 hover:text-white transition-colors">Login</Link>
              <Link to="/register" onClick={() => setIsOpen(false)} className="bg-emerald-500 text-center py-2 rounded-lg text-slate-950 font-bold hover:bg-emerald-600 transition-all">Sign Up</Link>
            </div>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;