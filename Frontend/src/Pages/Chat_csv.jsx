import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, FileUp, Database, Loader2, User, Bot, RefreshCw } from 'lucide-react';
import axios from 'axios';
import { toast } from 'react-toastify';

const Chat_csv = () => {
  const [file, setFile] = useState(null);
  const [isUploaded, setIsUploaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  
  const scrollRef = useRef(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, chatLoading]);

  const handleFileUpload = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await axios.post(
        'https://datasage-backend-jrjo.onrender.com/csv-chat/upload/',
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
            setFile(selectedFile);
      setIsUploaded(true);
      toast.success("CSV Engine Ready!");
      setMessages([{ role: 'bot', content: `Dataset "${selectedFile.name}" analyzed successfully. How can I assist your research today?` }]);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || chatLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setChatLoading(true);

    try {
      const response = await axios.post(
      `https://datasage-backend-jrjo.onrender.com/csv-chat/chat/?question=${encodeURIComponent(currentInput)}`,
      null,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
      setMessages(prev => [...prev, { role: 'bot', content: response.data.answer }]);
    } catch (err) {
      toast.error("Query processing error");
      setMessages(prev => [...prev, { role: 'bot', content: "Our diagnostic engine encountered an error. Please try again." }]);
    } finally {
      setChatLoading(false);
    }
  };

  const resetChat = () => {
    setFile(null);
    setIsUploaded(false);
    setMessages([]);
    setInput("");
  };

  return (
    <div className="h-[calc(100vh-64px)] bg-slate-950 text-white flex flex-col font-sans selection:bg-emerald-500/30">
      <div className="max-w-6xl mx-auto w-full h-full px-6 py-8 flex flex-col">
        
        <AnimatePresence mode="wait">
          {!isUploaded ? (
            <motion.div 
              key="upload"
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="flex-grow flex flex-col items-center justify-center border border-white/5 rounded-[3rem] bg-white/[0.01] shadow-2xl shadow-black"
            >
              <div className="p-10 bg-emerald-500/10 rounded-full mb-8 ring-1 ring-emerald-500/20">
                <Database className="text-emerald-400 w-12 h-12" />
              </div>
              <h2 className="text-4xl font-black mb-4 tracking-tighter">Query <span className="text-emerald-400 font-outline-2">Dataset</span></h2>
              <p className="text-gray-500 text-sm mb-10 font-bold uppercase tracking-[0.2em] not-italic">Natural Language Data Processing</p>
              
              <label className="cursor-pointer bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-black px-12 py-4 rounded-2xl flex items-center gap-3 transition-all active:scale-95 shadow-xl shadow-emerald-500/10">
                {loading ? <Loader2 className="animate-spin" /> : <FileUp size={20} />}
                <span className="text-xs uppercase tracking-widest">{loading ? "Synchronizing..." : "Initialize CSV Chat"}</span>
                <input type="file" className="hidden" accept=".csv" onChange={handleFileUpload} disabled={loading} />
              </label>
            </motion.div>
          ) : (
            <motion.div 
              key="chat"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex-grow flex flex-col bg-white/[0.02] border border-white/10 rounded-[2.5rem] overflow-hidden shadow-2xl"
            >
              <div className="px-8 py-6 border-b border-white/10 bg-white/[0.01] flex justify-between items-center">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 flex items-center justify-center text-emerald-400 border border-emerald-500/20">
                    <Database size={22} />
                  </div>
                  <div>
                    <h3 className="text-sm font-black not-italic tracking-tight">{file?.name}</h3>
                    <div className="flex items-center gap-2 mt-0.5">
                      <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                      <p className="text-[10px] text-emerald-500 font-black uppercase tracking-widest not-italic">Engine Active</p>
                    </div>
                  </div>
                </div>
                <button 
                  onClick={resetChat} 
                  className="flex items-center gap-2 px-5 py-2.5 bg-white/5 hover:bg-red-500/10 hover:text-red-400 border border-white/10 rounded-xl transition-all text-[10px] font-black uppercase tracking-widest"
                >
                  <RefreshCw size={14} /> New Query
                </button>
              </div>

              <div ref={scrollRef} className="flex-grow overflow-y-auto p-10 space-y-8 custom-scrollbar">
                {messages.map((msg, i) => (
                  <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`flex gap-5 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg ${msg.role === 'user' ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/20' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20'}`}>
                        {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
                      </div>
                      <div className={`p-5 rounded-[1.8rem] text-sm leading-relaxed font-semibold not-italic ${msg.role === 'user' ? 'bg-cyan-500/10 text-cyan-50 border border-cyan-500/20 rounded-tr-none' : 'bg-white/5 text-gray-200 border border-white/10 rounded-tl-none'}`}>
                        {msg.content}
                      </div>
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start animate-pulse">
                    <div className="w-10 h-10 rounded-xl bg-emerald-500/10 mr-5 border border-emerald-500/10"></div>
                    <div className="p-5 bg-white/5 rounded-2xl w-32 h-12 border border-white/10"></div>
                  </div>
                )}
              </div>

              <div className="p-8 bg-white/[0.01] border-t border-white/10">
                <form onSubmit={handleSendMessage} className="relative max-w-4xl mx-auto group">
                  <input 
                    type="text"
                    placeholder="Inquire about patterns, statistics, or anomalies..."
                    className="w-full bg-slate-900/50 border border-white/10 rounded-2xl py-5 pl-8 pr-16 focus:outline-none focus:border-emerald-500/50 focus:bg-slate-900 transition-all text-sm font-semibold not-italic placeholder:text-gray-600 shadow-inner"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                  />
                  <button 
                    disabled={!input.trim() || chatLoading}
                    className="absolute right-2.5 top-1/2 -translate-y-1/2 p-3.5 bg-emerald-500 hover:bg-emerald-600 disabled:bg-white/5 disabled:text-gray-600 text-slate-950 rounded-xl transition-all shadow-lg active:scale-95"
                  >
                    <Send size={20} />
                  </button>
                </form>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default Chat_csv;