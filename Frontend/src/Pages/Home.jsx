import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { BarChart3, MessageSquare, Zap, ShieldCheck, Globe, Cpu, ArrowRight } from 'lucide-react';

const Home = () => {
  return (
    <div className="bg-slate-950 text-white min-h-screen relative overflow-hidden">
      {/* Background Decorative Grid Pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] -z-10" />

      <div className="max-w-6xl mx-auto px-6 lg:px-10">
        
        {/* Hero Section */}
        <section className="relative pt-12 pb-16 text-center">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[400px] h-[400px] bg-emerald-500/10 blur-[100px] rounded-full -z-10" />
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/5 border border-emerald-500/20 text-emerald-400 text-[10px] font-bold mb-6 tracking-widest uppercase">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span>Production Level AI Agent Engine</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-black tracking-tighter mb-6 leading-[1.1]">
              Talk to Your Data with <br />
              <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                DataSage AI
              </span>
            </h1>
            <p className="text-gray-400 text-base md:text-lg max-w-xl mx-auto mb-10 leading-relaxed">
              Transform static CSV files into dynamic conversations. Experience the power 
              of automated data science and real-time visual insights.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link to="/register" className="w-full sm:w-auto px-8 py-4 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold rounded-2xl transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 active:scale-95">
                Get Started <ArrowRight size={20} />
              </Link>
              <Link to="/chat-csv" className="w-full sm:w-auto px-8 py-4 bg-white/5 border border-white/10 hover:bg-white/10 rounded-2xl transition-all backdrop-blur-md active:scale-95">
                Try Live Demo
              </Link>
            </div>
          </motion.div>
        </section>

        {/* Features Section */}
        <section className="pb-16 pt-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard 
              icon={<MessageSquare size={24} />}
              title="Natural Chat"
              desc="Ask questions in plain English and get instant analytical answers from your CSV datasets."
            />
            <FeatureCard 
              icon={<BarChart3 size={24} />}
              title="Smart Visuals"
              desc="Auto-generated interactive charts and graphs that bring your data patterns to life instantly."
            />
            <FeatureCard 
              icon={<Zap size={24} />}
              title="Fast Agent Logic"
              desc="High-performance backend built with FastAPI for lightning-fast row processing and automation."
            />
            <FeatureCard 
              icon={<ShieldCheck size={24} />}
              title="Secure Storage"
              desc="Enterprise-grade encryption and secure authentication to keep your private data protected."
            />
            <FeatureCard 
              icon={<Cpu size={24} />}
              title="AI Reports"
              desc="Receive detailed Markdown reports with trend detection and intelligent predictive summaries."
            />
            <FeatureCard 
              icon={<Globe size={24} />}
              title="Global Access"
              desc="Fully responsive design optimized for mobile, tablet, and professional desktop screens."
            />
          </div>
        </section>

        {/* Stunning Stats Section */}
        <section className="py-20 relative">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <StatItem 
              val="99.9%" 
              label="Model Precision" 
              sub="AI-Driven Accuracy"
              color="text-emerald-400"
            />
            <StatItem 
              val="24/7" 
              label="Agent Logic" 
              sub="MCP Automation" 
              color="text-cyan-400"
            />
            <StatItem 
              val="1M+" 
              label="Data Rows" 
              sub="Production DevOps" 
              color="text-emerald-400"
            />
            <StatItem 
              val="100%" 
              label="Responsive" 
              sub="Cross-Platform" 
              color="text-cyan-400"
            />
          </div>
        </section>

        {/* Final Stunning CTA Box */}
        <section className="pb-24 pt-4 text-center">
          <motion.div 
            whileHover={{ scale: 1.01 }}
            className="p-10 md:p-16 rounded-[2.5rem] bg-gradient-to-b from-white/5 to-transparent border border-white/10 relative overflow-hidden group shadow-2xl"
          >
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-64 bg-emerald-500/10 blur-[80px] rounded-full -z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
            
            <h2 className="text-3xl md:text-5xl font-black mb-6 tracking-tight">Ready to talk to your data?</h2>
            <p className="text-gray-400 mb-10 max-w-lg mx-auto leading-relaxed text-sm md:text-base">
              Join developers and data scientists using DataSage to automate their data workflows. 
              Start your first AI-driven conversation today.
            </p>
            <Link to="/register" className="inline-flex items-center px-10 py-4 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-black rounded-2xl transition-all shadow-[0_0_40px_rgba(16,185,129,0.2)] hover:scale-105 active:scale-95">
              Launch DataSage Now
            </Link>
          </motion.div>
        </section>

      </div>
    </div>
  );
};

const FeatureCard = ({ icon, title, desc }) => (
  <motion.div 
    whileHover={{ y: -5, borderColor: 'rgba(16,185,129,0.3)' }}
    className="p-8 rounded-3xl bg-white/[0.03] border border-white/10 hover:bg-white/[0.07] transition-all flex flex-col items-start text-left group h-full shadow-xl"
  >
    <div className="mb-5 p-3 bg-slate-900 rounded-2xl text-emerald-400 ring-1 ring-white/10 group-hover:bg-emerald-500 group-hover:text-slate-950 transition-all duration-300">
      {icon}
    </div>
    <h3 className="text-xl font-bold mb-3 tracking-tight group-hover:text-emerald-400 transition-colors">{title}</h3>
    <p className="text-gray-400 text-sm leading-relaxed opacity-80">
      {desc}
    </p>
  </motion.div>
);

const StatItem = ({ val, label, sub, color }) => (
  <motion.div 
    initial={{ opacity: 0, scale: 0.9 }}
    whileInView={{ opacity: 1, scale: 1 }}
    viewport={{ once: true }}
    className="relative group p-6 rounded-3xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.05] transition-all text-center"
  >
    <div className={`text-4xl md:text-5xl font-black ${color} tracking-tighter mb-2 group-hover:scale-105 transition-transform duration-300`}>
      {val}
    </div>
    <div className="text-white font-bold text-[10px] uppercase tracking-[0.2em] mb-1">{label}</div>
    <div className="text-gray-600 text-[9px] font-medium tracking-tight">{sub}</div>
  </motion.div>
);

export default Home;