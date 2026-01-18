import React, { useState } from 'react';
import axios from 'axios';
import Chart from 'react-apexcharts';
import { motion } from 'framer-motion';
import { 
  FileUp, Zap, LayoutDashboard, Loader2, RefreshCw, 
  FileText, Download, ShieldAlert, CheckCircle2, 
  BarChart3, Columns, Hash, Activity
} from 'lucide-react';
import { toast } from 'react-toastify';

const Insight = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const token = localStorage.getItem('token');

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('https://datasage-backend-jrjo.onrender.com/upload/upload-csv/', formData, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data' 
        }
      });
      if (response.data?.result) {
        setData(response.data.result);
        toast.success("Intelligence Report Generated!");
      }
    } catch (err) {
      console.error("Upload error:", err);
      toast.error("Upload failed. Verify API connection.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingScreen />;
  if (!data) return <UploadScreen handleUpload={handleUpload} />;

  const displayCharts = data.charts?.charts
    ?.filter(chart => chart.type !== 'boxplot')
    ?.slice(0, 6) || [];

  return (
    <div className="bg-slate-950 min-h-screen text-white pb-24 selection:bg-emerald-500/30 font-sans">
      <div className="max-w-6xl mx-auto px-6 pt-10 space-y-12">
        
        {/* HEADER SECTION - Clean & Balanced */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div className="space-y-1">
            <h1 className="text-3xl font-black tracking-tighter">Diagnostic <span className="text-emerald-400">Intelligence</span></h1>
            <p className="text-gray-500 text-[10px] font-black uppercase tracking-[0.3em] not-italic">Advanced Pattern Analysis</p>
          </div>
          <div className="flex gap-4">
            <button onClick={() => setData(null)} className="flex items-center gap-2 bg-white/5 border border-white/10 px-5 py-2.5 rounded-xl hover:bg-white/10 transition-all font-bold text-[10px] uppercase tracking-widest not-italic">
              <RefreshCw size={14} className="text-gray-500" /> New Scan
            </button>
            <button className="flex items-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-slate-950 px-6 py-2.5 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-xl shadow-emerald-500/10 active:scale-95 not-italic">
              <Download size={16} /> Export MD
            </button>
          </div>
        </div>


        <div className="grid grid-cols-2 lg:grid-cols-4 gap-5">
          <StatTab icon={<Hash size={16}/>} label="Total Rows" value={data.metadata?.rows} color="emerald" />
          <StatTab icon={<Columns size={16}/>} label="Data Features" value={data.metadata?.columns?.length} color="cyan" />
          <StatTab icon={<Activity size={16}/>} label="Risk Mean" value={data.eda?.summary_statistics?.cvd_risk_score?.mean?.toFixed(2) || "N/A"} color="yellow" />
          <StatTab icon={<Zap size={16}/>} label="Status" value="Ready" color="emerald" />
        </div>

        {/* AI REPORT SECTION */}
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Summary - Seedha & Bold Text */}
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="lg:col-span-2 bg-white/[0.02] border border-white/10 p-10 rounded-[2.5rem] shadow-2xl relative overflow-hidden group">
              <h3 className="text-[10px] font-black uppercase text-gray-500 tracking-[0.2em] mb-6 not-italic">Executive Summary</h3>
              <p className="text-gray-200 text-lg leading-relaxed font-semibold not-italic border-l-4 border-emerald-500/20 pl-8">
                {data.insights?.summary || "No summary available."}
              </p>
            </motion.div>

            {/* Key Findings Sidebox */}
            <div className="bg-emerald-500/5 border border-emerald-500/10 p-10 rounded-[2.5rem]">
               <h3 className="text-[10px] font-black uppercase text-emerald-400 tracking-[0.2em] mb-8 not-italic">Key Findings</h3>
               <div className="space-y-5">
                 {data.insights?.key_insights?.slice(0, 3).map((ki, i) => (
                   <div key={i} className="flex gap-4">
                     <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 mt-2 shadow-[0_0_8px_#10b981]" />
                     <p className="text-xs text-gray-400 font-bold leading-snug not-italic">{ki}</p>
                   </div>
                 )) || <p className="text-gray-500 text-xs font-bold not-italic">No insights available.</p>}
               </div>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-red-500/[0.03] border border-red-500/10 p-10 rounded-[2.5rem]">
              <div className="flex items-center gap-3 mb-8">
                <div className="p-2 bg-red-500/20 rounded-lg text-red-400"><ShieldAlert size={22} /></div>
                <h4 className="text-xs font-black uppercase tracking-widest text-red-400 not-italic">Critical Risks</h4>
              </div>
              <div className="space-y-4">
                {data.insights?.risks?.map((r, i) => (
                  <div key={i} className="flex gap-4 bg-white/5 p-4 rounded-2xl border border-white/5">
                    <span className="text-red-500 font-black">•</span>
                    <p className="text-gray-300 text-xs font-bold leading-snug not-italic">{r}</p>
                  </div>
                )) || <p className="text-gray-500 text-xs font-bold not-italic">No risks identified.</p>}
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-emerald-500/[0.03] border border-emerald-500/10 p-10 rounded-[2.5rem]">
              <div className="flex items-center gap-3 mb-8">
                <div className="p-2 bg-emerald-500/20 rounded-lg text-emerald-400"><CheckCircle2 size={22} /></div>
                <h4 className="text-xs font-black uppercase tracking-widest text-emerald-400 not-italic">Strategic Actions</h4>
              </div>
              <div className="space-y-4">
                {data.insights?.recommendations?.map((r, i) => (
                  <div key={i} className="flex gap-4 bg-white/5 p-4 rounded-2xl border border-white/5">
                    <span className="text-emerald-500 font-black">→</span>
                    <p className="text-gray-300 text-xs font-bold leading-snug not-italic">{r}</p>
                  </div>
                )) || <p className="text-gray-500 text-xs font-bold not-italic">No recommendations available.</p>}
              </div>
            </div>
          </div>
        </div>

        {/* VISUALIZATIONS GRID */}
        <div className="space-y-10 pt-10">
          <h2 className="text-2xl font-black flex items-center gap-4 tracking-tight not-italic">
            <BarChart3 className="text-emerald-400" /> Statistical Dashboards
          </h2>
          {displayCharts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
              {displayCharts.map((chart, i) => (
                <div key={i} className="bg-slate-900/40 border border-white/10 p-10 rounded-[3rem] shadow-xl hover:border-emerald-500/30 transition-all group">
                  <h3 className="text-[10px] font-black text-gray-500 uppercase tracking-[0.2em] mb-8 border-l-4 border-emerald-500/40 pl-5 group-hover:text-emerald-400 transition-colors not-italic">
                    {chart.title}
                  </h3>
                  <ChartRenderer chart={chart} />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-20 border border-dashed border-white/10 rounded-[3rem]">
              <p className="text-gray-500 font-bold uppercase tracking-widest text-xs not-italic">Visual Data Engine on Standby</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};


const ChartRenderer = ({ chart }) => {
  const isBar = chart.type === 'bar';
  const isScatter = chart.type === 'scatter';
  const isHeatmap = chart.type === 'heatmap';
  const isHist = chart.type === 'histogram';

  const options = {
    chart: { 
      background: 'transparent', 
      toolbar: { show: false }, 
      animations: { enabled: true, speed: 600, animateGradually: { enabled: true } },
      zoom: { enabled: false },
      fontFamily: 'inherit'
    },
    theme: { mode: 'dark' },
    colors: ['#10b981', '#06b6d4', '#8b5cf6', '#f59e0b'],
    xaxis: { 
      labels: { style: { colors: '#64748b', fontSize: '10px', fontWeight: 800 } },
      axisBorder: { show: false },
      axisTicks: { show: false }
    },
    yaxis: { 
      labels: { style: { colors: '#64748b', fontSize: '10px', fontWeight: 600 } }
    },
    grid: { 
      borderColor: '#1e293b', 
      strokeDashArray: 3,
      xaxis: { lines: { show: false } },
      yaxis: { lines: { show: true } }
    },
    dataLabels: { enabled: false },
    tooltip: { theme: 'dark' },
  };

  let series = [];
  let chartType = 'line';

  if (isBar || isHist) {
    chartType = 'bar';
    if (isHist && chart.data) {
      const max = Math.max(...chart.data);
      const min = Math.min(...chart.data);
      const binCount = 20;
      const binWidth = (max - min) / binCount;
      const bins = Array(binCount).fill(0);
      const categories = [];
      chart.data.forEach(value => {
        const binIndex = Math.min(Math.floor((value - min) / binWidth), binCount - 1);
        bins[binIndex]++;
      });
      for (let i = 0; i < binCount; i++) {
        const start = min + (i * binWidth);
        categories.push(`${start.toFixed(1)}`);
      }
      options.xaxis.categories = categories;
      series = [{ name: 'Frequency', data: bins }];
    } else {
      series = [{ name: 'Values', data: chart.data || [] }];
    }
  } else if (isScatter) {
    chartType = 'scatter';
    if (chart.x && chart.y) {
      series = [{ name: 'Correlation', data: chart.x.map((xVal, index) => [xVal, chart.y[index]]) }];
    }
  } else if (isHeatmap) {
    chartType = 'heatmap';
    if (chart.z && chart.x && chart.y) {
      series = chart.z.map((row, i) => ({
        name: chart.y[i],
        data: row.map((value, j) => ({ x: chart.x[j], y: value }))
      }));
    }
  }

  return <Chart options={options} series={series} type={chartType} height={300} width="100%" />;
};

const StatTab = ({ icon, label, value, color }) => {
  const colorClasses = {
    emerald: 'bg-emerald-500/10 text-emerald-400 ring-emerald-500/20',
    cyan: 'bg-cyan-500/10 text-cyan-400 ring-cyan-500/20',
    yellow: 'bg-yellow-500/10 text-yellow-400 ring-yellow-500/20',
  };
  return (
    <div className="bg-white/[0.02] border border-white/10 p-6 rounded-[2rem] flex items-center gap-5 group hover:bg-white/5 transition-all">
      <div className={`p-4 rounded-2xl ${colorClasses[color]} ring-1 shadow-lg shadow-black/20 group-hover:scale-110 transition-transform`}>
        {icon}
      </div>
      <div>
        <p className="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-1 not-italic">{label}</p>
        <p className="text-2xl font-black tracking-tighter not-italic">{value || 0}</p>
      </div>
    </div>
  );
};

const UploadScreen = ({ handleUpload }) => (
  <div className="min-h-[85vh] flex flex-col items-center justify-center text-center px-6 bg-slate-950">
    <div className="bg-emerald-500/10 p-12 rounded-full mb-10 ring-1 ring-emerald-500/20 shadow-[0_0_50px_rgba(16,185,129,0.1)]">
      <LayoutDashboard size={48} className="text-emerald-400" />
    </div>
    <h1 className="text-5xl font-black tracking-tighter mb-6 not-italic">
      Insight <span className="text-emerald-400 font-outline-2 text-6xl">Studio.</span>
    </h1>
    <p className="text-gray-500 text-sm mb-12 max-w-sm font-bold uppercase tracking-[0.2em] leading-relaxed not-italic">
      Professional Data Diagnostic Agent
    </p>
    <label className="cursor-pointer bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-black px-12 py-5 rounded-2xl shadow-xl shadow-emerald-500/20 active:scale-95 transition-all text-xs uppercase tracking-widest flex items-center gap-3 not-italic">
      <FileUp size={18} /> Initialize Analysis
      <input type="file" className="hidden" accept=".csv" onChange={handleUpload} />
    </label>
  </div>
);

const LoadingScreen = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950">
    <div className="relative mb-10">
      <div className="w-24 h-24 border-2 border-emerald-500/10 border-t-emerald-500 rounded-full animate-spin" />
      <Zap className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-emerald-400 animate-pulse" size={32} />
    </div>
    <h2 className="text-2xl font-bold tracking-tight text-white uppercase tracking-[0.3em] not-italic">Processing Dataset</h2>
    <p className="text-gray-500 mt-4 text-[10px] animate-pulse font-black uppercase tracking-widest not-italic">Synchronizing Patterns</p>
  </div>
);

export default Insight;