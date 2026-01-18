import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Mail, User, MessageSquare, Tag, Loader2, Sparkles, MapPin } from 'lucide-react';
import axios from 'axios';
import { toast } from 'react-toastify';

const Contact = () => {
  const [formData, setFormData] = useState({ name: '', email: '', topic: '', message: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('https://datasage-backend-jrjo.onrender.com/contact/send', formData);
      toast.success(response.data.message);
      setFormData({ name: '', email: '', topic: '', message: '' });
    } catch (err) {
      toast.error(err.response?.data?.detail || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white relative py-10 overflow-hidden">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-emerald-500/5 blur-[120px] rounded-full -z-10" />
      <div className="max-w-6xl mx-auto px-6 sm:px-10 space-y-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-bold tracking-widest uppercase">
              <Sparkles size={12} />
              <span>Get in Touch</span>
            </div>
            
            <h1 className="text-4xl md:text-7xl font-black tracking-tighter leading-none">
              Let's <span className="text-emerald-400">Connect.</span>
            </h1>
            
            <p className="text-gray-400 text-base md:text-lg leading-relaxed max-w-md">
              Have a project in mind or need help with DataSage? Drop a message and let's build something intelligent together.
            </p>

            <div className="space-y-4 pt-4">
              <div className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/10 w-fit">
                <Mail className="text-emerald-400" size={20} />
                <div>
                  <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">Email Me</p>
                  <p className="text-sm font-medium">Warishayat666@gmail.com</p>
                </div>
              </div>

              <div className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/10 w-fit">
                <MapPin className="text-cyan-400" size={20} />
                <div>
                  <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">Location</p>
                  <p className="text-sm font-medium">Islamabad, Pakistan</p>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white/[0.02] border border-white/10 p-8 rounded-[2rem] backdrop-blur-xl shadow-2xl relative group"
          >
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input icon={<User size={18}/>} placeholder="Name" value={formData.name} onChange={(val) => setFormData({...formData, name: val})} />
                <Input icon={<Mail size={18}/>} placeholder="Email" type="email" value={formData.email} onChange={(val) => setFormData({...formData, email: val})} />
              </div>
              <Input icon={<Tag size={18}/>} placeholder="Topic / Subject" value={formData.topic} onChange={(val) => setFormData({...formData, topic: val})} />
              
              <div className="relative group">
                <MessageSquare className="absolute left-4 top-4 text-gray-500 group-focus-within:text-emerald-400 transition-colors" size={18} />
                <textarea 
                  rows="4"
                  placeholder="Tell me about your project..."
                  className="w-full bg-slate-900/50 border border-white/10 rounded-2xl py-3.5 pl-12 pr-4 focus:outline-none focus:border-emerald-400 transition-all text-sm resize-none"
                  value={formData.message}
                  onChange={(e) => setFormData({...formData, message: e.target.value})}
                  required
                />
              </div>

              <button 
                disabled={loading} 
                className="w-full py-4 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-black rounded-2xl transition-all shadow-lg flex items-center justify-center gap-2 active:scale-95 disabled:opacity-50"
              >
                {loading ? <Loader2 className="animate-spin" /> : <>Send Message <Send size={18}/></>}
              </button>
            </form>
          </motion.div>
        </div>

        {/* Map Section - Contained in the same margins */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-[2rem] overflow-hidden border border-white/10 shadow-2xl h-[350px] relative group"
        >
          <iframe 
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d106203.204561706!2d72.91684784335936!3d33.6844201!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38dfbfd07891722f%3A0x6059515c3bdb02b6!2sIslamabad%2C%20Islamabad%20Capital%20Territory!5e0!3m2!1sen!2spk!4v1700000000000!5m2!1sen!2spk"
            width="100%" 
            height="100%" 
            style={{ border: 0, filter: 'invert(90%) hue-rotate(180deg) brightness(0.9) contrast(0.9)' }} 
            allowFullScreen="" 
            loading="lazy" 
            title="Islamabad Map"
          />
          <div className="absolute inset-0 pointer-events-none border border-white/10 rounded-[2rem]" />
        </motion.div>

      </div>
    </div>
  );
};

const Input = ({ icon, placeholder, type = "text", value, onChange }) => (
  <div className="relative group">
    <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-emerald-400 transition-colors">
      {icon}
    </div>
    <input 
      type={type} 
      placeholder={placeholder}
      className="w-full bg-slate-900/50 border border-white/10 rounded-2xl py-3.5 pl-12 pr-4 focus:outline-none focus:border-emerald-500 transition-all text-sm"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      required
    />
  </div>
);

export default Contact;