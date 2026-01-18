import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-slate-950 border-t border-white/5 py-12 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 text-center md:text-left">
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-2">
            <h2 className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent mb-4">
              DataSage
            </h2>
            <p className="text-gray-400 max-w-sm mx-auto md:mx-0">
              Empowering developers and data scientists with AI-driven insights. 
              Turn your complex CSV files into meaningful conversations.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-bold uppercase tracking-wider text-emerald-400 mb-4">Product</h3>
            <ul className="space-y-2">
              <li><Link to="/chat-csv" className="text-gray-400 hover:text-white transition-colors">Chat CSV</Link></li>
              <li><Link to="/insights" className="text-gray-400 hover:text-white transition-colors">Insights</Link></li>
              <li><Link to="/" className="text-gray-400 hover:text-white transition-colors">Docs</Link></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-sm font-bold uppercase tracking-wider text-emerald-400 mb-4">Company</h3>
            <ul className="space-y-2">
              <li><Link to="/contact" className="text-gray-400 hover:text-white transition-colors">Contact</Link></li>
              <li><Link to="/" className="text-gray-400 hover:text-white transition-colors">Privacy</Link></li>
            </ul>
          </div>
        </div>
        
        {/* Bottom Section - Centered */}
        <div className="mt-12 pt-8 border-t border-white/5 text-center">
          <p className="text-sm text-gray-500">
            © {new Date().getFullYear()} DataSage. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;