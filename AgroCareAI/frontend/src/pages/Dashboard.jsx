import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, CheckCircle2, AlertCircle, Info, Loader2, Microscope, Activity, ShieldAlert, FileText } from 'lucide-react';
import api from '../services/api';
import { toast } from 'react-toastify';

const Dashboard = () => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [activeCard, setActiveCard] = useState(null);

    const onDrop = useCallback((acceptedFiles) => {
        const file = acceptedFiles[0];
        if (file) {
            setFile(file);
            setPreview(URL.createObjectURL(file));
            setResult(null);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.jpeg', '.jpg', '.png', '.webp']
        },
        maxFiles: 1,
        multiple: false
    });

    const removeFile = (e) => {
        e.stopPropagation();
        setFile(null);
        setPreview(null);
        setResult(null);
    };

    const handleDiagnose = async () => {
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await api.post('/predict', formData);
            setResult(response.data);
            toast.success("Analysis Complete");
        } catch (error) {
            console.error(error);
            toast.error(error.response?.data?.error || "Analysis failed. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen text-gray-100 py-12 px-4 sm:px-6 lg:px-8 font-sans">
            <div className="max-w-6xl mx-auto">
                <div className="mb-10">
                    <h1 className="text-3xl font-extrabold text-white mb-2">Diagnostic <span className="text-emerald-600">Lab</span></h1>
                    <p className="text-emerald-50/70 font-medium">Upload plant samples for real-time tissue analysis and disease detection.</p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
                    {/* Left Column: Upload */}
                    <div className="lg:col-span-1 space-y-6">
                        <div className="glass-panel p-8 relative overflow-hidden">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/20 rounded-full blur-xl -mr-16 -mt-16 z-0"></div>

                            <div className="relative z-10">
                                <h2 className="text-lg font-bold mb-6 text-white flex items-center">
                                    <Microscope className="h-5 w-5 mr-3 text-emerald-600" />
                                    Sample Upload
                                </h2>

                                <div
                                    {...getRootProps()}
                                    className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all relative h-72 flex flex-col items-center justify-center ${isDragActive ? 'border-emerald-400 bg-emerald-500/20 scale-[1.02]' : 'border-white/20 hover:border-emerald-400 hover:bg-white/5'
                                        }`}
                                >
                                    <input {...getInputProps()} />

                                    {preview ? (
                                        <div className="relative w-full h-full flex items-center justify-center">
                                            <img src={preview} alt="Preview" className="max-h-full max-w-full rounded-xl object-contain shadow-md" />
                                            <button
                                                onClick={removeFile}
                                                className="absolute -top-3 -right-3 bg-slate-900 border-2 border-white text-white rounded-full p-2 hover:bg-red-600 transition-all hover:rotate-90"
                                            >
                                                <X className="h-3 w-3" />
                                            </button>
                                        </div>
                                    ) : (
                                        <>
                                            <div className="bg-black/30 p-4 rounded-full border border-white/10 mb-4 border border-slate-100 group-hover:scale-110 transition-transform">
                                                <Upload className={`h-8 w-8 ${isDragActive ? 'text-emerald-600' : 'text-gray-400'}`} />
                                            </div>
                                            <p className="text-white font-bold mb-1">
                                                {isDragActive ? "Drop to scan" : "Click or drag source"}
                                            </p>
                                            <p className="text-gray-400 text-xs">High-res JPEG, PNG, WEBP</p>
                                        </>
                                    )}
                                </div>

                                <button
                                    onClick={handleDiagnose}
                                    disabled={!file || loading}
                                    className="w-full mt-8 flex justify-center items-center py-4 px-6 rounded-2xl shadow-xl shadow-emerald-200 text-sm font-black text-white glass-button focus:outline-none focus:ring-4 focus:ring-emerald-500/50 disabled:opacity-30 disabled:shadow-none transition-all active:scale-95"
                                >
                                    {loading ? (
                                        <>
                                            <Loader2 className="animate-spin -ml-1 mr-3 h-5 w-5" />
                                            Neural Processing...
                                        </>
                                    ) : (
                                        <>
                                            <Activity className="h-4 w-4 mr-3" />
                                            Analyze Sample
                                        </>
                                    )}
                                </button>
                            </div>
                        </div>

                        <div className="glass-panel bg-black/40 p-6 shadow-none">
                            <div className="flex items-center gap-3 mb-3">
                                <div className="p-2 bg-white/10 rounded-lg">
                                    <Info className="h-4 w-4 text-emerald-400" />
                                </div>
                                <h4 className="font-bold text-sm">Pro Tip</h4>
                            </div>
                            <p className="text-xs text-gray-400 leading-relaxed font-medium">
                                Ensure the leaf surface is well-lit and covers at least 60% of the frame for maximum diagnostic accuracy.
                            </p>
                        </div>
                    </div>

                    {/* Right Column: Results */}
                    <div className="lg:col-span-2">
                        <div className="glass-panel p-10 h-full min-h-[500px] flex flex-col">
                            <h2 className="text-lg font-bold mb-8 text-white flex items-center">
                                <FileText className="h-5 w-5 mr-3 text-emerald-600" />
                                Analysis Report
                            </h2>

                            {result ? (
                                <div className="animate-in fade-in slide-in-from-bottom-5 duration-700 flex-grow flex flex-col">
                                    {/* Main Result Card */}
                                    <div className={`p-8 rounded-3xl mb-8 flex flex-col sm:flex-row items-center gap-8 border-l-[12px] ${result.health_status === 'Healthy'
                                            ? 'glass-panel bg-emerald-500/20 border-emerald-400 shadow-[0_0_20px_rgba(52,211,153,0.3)]'
                                            : 'glass-panel bg-red-500/20 border-red-400 shadow-[0_0_20px_rgba(248,113,113,0.3)]'
                                        }`}>
                                        <div className={`p-6 rounded-2xl shadow-inner ${result.health_status === 'Healthy' ? 'bg-emerald-500/30 border border-emerald-400/50' : 'bg-red-500/30 border border-red-400/50'
                                            }`}>
                                            {result.health_status === 'Healthy' ? (
                                                <CheckCircle2 className="h-12 w-12 text-emerald-600" />
                                            ) : (
                                                <ShieldAlert className="h-12 w-12 text-red-600" />
                                            )}
                                        </div>
                                        <div className="text-center sm:text-left flex-grow">
                                            <div className="flex items-center gap-3 mb-1 justify-center sm:justify-start">
                                                <span className={`text-[10px] font-black uppercase tracking-widest px-2 py-0.5 rounded-md ${result.health_status === 'Healthy' ? 'bg-emerald-500/30 text-emerald-100 border border-emerald-400/30' : 'bg-red-500/30 text-red-100 border border-red-400/30'
                                                    }`}>
                                                    System Level Result
                                                </span>
                                            </div>
                                            <h3 className={`text-4xl font-black ${result.health_status === 'Healthy' ? 'text-emerald-300 drop-shadow-md' : 'text-red-300 drop-shadow-md'}`}>
                                                {result.health_status === 'Diseased' ? 'Diseased Leaf' : 'Healthy Leaf'}
                                            </h3>
                                            <div className="mt-3 flex items-center gap-2 justify-center sm:justify-start">
                                                <div className="flex bg-slate-200 h-2 w-32 rounded-full overflow-hidden">
                                                    <div
                                                        className={`h-full ${result.health_status === 'Healthy' ? 'bg-emerald-500' : 'bg-red-500'}`}
                                                        style={{ width: `${result.confidence}%` }}
                                                    ></div>
                                                </div>
                                                <span className="text-xs font-bold text-emerald-100/80">
                                                    Confidence: {result.confidence.toFixed(1)}%
                                                </span>
                                            </div>

                                            {result.health_status === 'Diseased' && (
                                                <div className="mt-6 space-y-4">
                                                    <div className="p-4 bg-red-500/30 border border-red-400/50/50 rounded-2xl border border-red-200">
                                                        <p className="text-sm font-bold text-red-300 drop-shadow-md">
                                                            Disease Category: <span className="capitalize">{result.disease_category}</span>
                                                        </p>
                                                    </div>
                                                    {result.knowledge_base && typeof result.knowledge_base === 'string' && (
                                                        <div className="p-4 bg-black/30 backdrop-blur-md rounded-2xl border border-white/10 overflow-hidden mt-6">
                                                            <p className="text-[10px] font-black text-gray-400 mb-2 uppercase tracking-widest flex items-center gap-2">
                                                                <FileText className="h-3 w-3" />
                                                                Knowledge Base Report
                                                            </p>
                                                            <pre className="text-xs text-gray-200 whitespace-pre-wrap font-mono overflow-auto max-h-64">
                                                                {result.knowledge_base}
                                                            </pre>
                                                        </div>
                                                    )}
                                                    {result.knowledge_base && typeof result.knowledge_base === 'object' && (
                                                        <div className="mt-6 space-y-4">
                                                            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest flex items-center gap-2 border-b pb-2">
                                                                <FileText className="h-3 w-3" /> Detailed Analysis Report
                                                            </p>

                                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="desc" baseClasses="glass-panel p-4">
                                                                    <h4 className="font-bold text-white text-sm mb-1 flex items-center gap-2">📝 Description</h4>
                                                                    <p className="text-xs text-emerald-100/80">{result.description}</p>
                                                                </InteractiveCard>

                                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="what" baseClasses="glass-panel p-4">
                                                                    <h4 className="font-bold text-white text-sm mb-1 flex items-center gap-2">🔍 What is it?</h4>
                                                                    <p className="text-xs text-emerald-100/80">{result.knowledge_base.detailed_explanation?.what_is_it || "Information not found."}</p>
                                                                </InteractiveCard>
                                                            </div>

                                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="risk" baseClasses="glass-panel bg-red-500/10 p-4 border-red-400/30">
                                                                    <h4 className="font-bold text-red-300 drop-shadow-md text-sm mb-2 flex items-center gap-2">🚨 Severity & Risk</h4>
                                                                    <div className="text-xs text-red-800 space-y-1 mt-3">
                                                                        <p><strong>System Risk Score:</strong> {result.confidence?.toFixed(1)}%</p>
                                                                        <p><strong>Disease Severity:</strong> {result.knowledge_base.severity_level || "Unknown"}</p>
                                                                        <p><strong>Spread Velocity:</strong> {result.knowledge_base.spread_risk || "Unknown"}</p>
                                                                    </div>
                                                                </InteractiveCard>

                                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="symptoms" baseClasses="glass-panel bg-amber-500/10 p-4 border-amber-400/30">
                                                                    <h4 className="font-bold text-amber-900 text-sm mb-2 flex items-center gap-2">⚠️ Symptoms</h4>
                                                                    <div className="text-xs text-amber-800 space-y-2">
                                                                        {result.knowledge_base.symptoms ? (
                                                                            <>
                                                                                {result.knowledge_base.symptoms.leaf_symptoms && <p><strong>Leaves:</strong> {result.knowledge_base.symptoms.leaf_symptoms}</p>}
                                                                                {result.knowledge_base.symptoms.stem_symptoms && <p><strong>Stem:</strong> {result.knowledge_base.symptoms.stem_symptoms}</p>}
                                                                                {result.knowledge_base.symptoms.fruit_symptoms && <p><strong>Fruit:</strong> {result.knowledge_base.symptoms.fruit_symptoms}</p>}
                                                                            </>
                                                                        ) : (
                                                                            <p>Symptoms information unavailable.</p>
                                                                        )}
                                                                    </div>
                                                                </InteractiveCard>
                                                            </div>

                                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="causes" baseClasses="glass-panel p-4">
                                                                    <h4 className="font-bold text-white text-sm mb-2 flex items-center gap-2">🧬 Causes</h4>
                                                                    <p className="text-xs text-emerald-100/80 mb-1">{result.knowledge_base.causes?.biological_or_environmental || "Information not found."}</p>
                                                                    {result.knowledge_base.causes?.weather_conditions && (
                                                                        <p className="text-xs text-emerald-100/80 mb-1"><strong>Weather:</strong> {result.knowledge_base.causes.weather_conditions}</p>
                                                                    )}
                                                                </InteractiveCard>

                                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="prevention" baseClasses="glass-panel p-4">
                                                                    <h4 className="font-bold text-white text-sm mb-2 flex items-center gap-2">🛡️ Precautions & Prevention</h4>
                                                                    {result.precautions && result.precautions.length > 0 ? (
                                                                        <ul className="text-xs text-emerald-100/80 list-disc ml-4 space-y-1">
                                                                            {result.precautions.map((prec, idx) => (
                                                                                <li key={idx}>{prec}</li>
                                                                            ))}
                                                                        </ul>
                                                                    ) : (
                                                                        <p className="text-xs text-emerald-100/80 italic">No specific precautions available.</p>
                                                                    )}
                                                                </InteractiveCard>
                                                            </div>

                                                            {result.knowledge_base.is_critical ? (
                                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="treatment" baseClasses="p-5 bg-red-500/30 border border-red-400/50 rounded-2xl shadow-inner border-2 border-red-300 mt-4">
                                                                    <h4 className="font-bold text-red-300 drop-shadow-md text-lg mb-2 flex items-center gap-2">❌ Plant Not Suitable</h4>
                                                                    <p className="text-sm text-red-800 font-medium">⚠️ This plant is not suitable to keep. There is no solution to cure it at this stage. Please remove and destroy this plant immediately.</p>
                                                                </InteractiveCard>
                                                            ) : (
                                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="treatment" baseClasses="glass-panel bg-emerald-500/10 p-5 border-emerald-400/30 mt-4">
                                                                    <h4 className="font-bold text-emerald-300 drop-shadow-md text-sm mb-3 flex items-center gap-2">💊 Treatment Steps</h4>
                                                                    {result.treatment && result.treatment.length > 0 ? (
                                                                        <ul className="text-xs text-emerald-700 list-disc ml-4 space-y-1">
                                                                            {result.treatment.map((treat, idx) => (
                                                                                <li key={idx} className={treat.includes("⚠️") ? "text-red-600 font-bold" : ""}>
                                                                                    {treat}
                                                                                </li>
                                                                            ))}
                                                                        </ul>
                                                                    ) : (
                                                                        <p className="text-xs text-emerald-700 italic">No specific treatments available.</p>
                                                                    )}
                                                                </InteractiveCard>
                                                            )}

                                                            {result.knowledge_base.additional_farmer_tips && (
                                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="tips" baseClasses="glass-panel bg-indigo-500/10 p-4 border-indigo-400/30 mt-4">
                                                                    <h4 className="font-bold text-indigo-900 text-sm mb-1 flex items-center gap-2">🧑‍🌾 Farmer Tip</h4>
                                                                    <p className="text-xs text-indigo-800 italic">{result.knowledge_base.additional_farmer_tips}</p>
                                                                </InteractiveCard>
                                                            )}
                                                        </div>
                                                    )}
                                                    {result.highlighted_image && (
                                                        <div className="animate-in zoom-in-95 duration-500">
                                                            <p className="text-[10px] font-black text-gray-400 mb-3 uppercase tracking-widest flex items-center gap-2">
                                                                <Activity className="h-3 w-3" />
                                                                Infection Visualization (Grad-CAM)
                                                            </p>
                                                            <div className="relative group">
                                                                <div className="absolute -inset-1 bg-gradient-to-r from-red-500 to-amber-500 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
                                                                <img 
                                                                    src={result.highlighted_image} 
                                                                    alt="Infection Heatmap" 
                                                                    className="relative w-full rounded-2xl shadow-2xl border-2 border-white object-cover aspect-video sm:aspect-auto" 
                                                                />
                                                            </div>
                                                        </div>
                                                    )}
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    <div className="flex-grow"></div>

                                    <div className="mt-8 flex justify-between items-center text-[10px] font-black uppercase tracking-tighter text-gray-400">
                                        <span>Scan Verified: {result.scan_id}</span>
                                        <span>Timestamp: {new Date().toLocaleTimeString()}</span>
                                    </div>
                                </div>
                            ) : (
                                <div className="flex-grow flex flex-col items-center justify-center text-gray-400 border-4 border-dashed border-white/10 rounded-[3rem] p-10">
                                    <div className="bg-black/30 p-6 rounded-full border border-white/10 mb-6 border border-slate-100">
                                        <Microscope className="h-10 w-10 text-slate-200" />
                                    </div>
                                    <p className="font-bold text-gray-400 text-center max-w-xs">
                                        Sample queue empty. Please upload an image to generate a diagnostic report.
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

const MetricItem = ({ label, value, status }) => (
    <div className="bg-slate-50 p-5 rounded-2xl border border-slate-100">
        <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest mb-1">{label}</p>
        <p className={`text-lg font-bold ${status === 'danger' ? 'text-red-600' : status === 'warning' ? 'text-amber-600' : 'text-emerald-600'
            }`}>
            {value}
        </p>
    </div>
);

const InteractiveCard = ({ id, activeCard, setActiveCard, children, baseClasses }) => {
    const isActive = activeCard === id;
    const [isBlinking, setIsBlinking] = useState(false);

    const handleClick = () => {
        if (!isActive) {
            setIsBlinking(true);
            setTimeout(() => setIsBlinking(false), 400); // 1-2 blinks duration
            setActiveCard(id);
        } else {
            setActiveCard(null); // click again to deselect
        }
    };

    return (
        <div 
            onClick={handleClick}
            className={`
                cursor-pointer transition-all duration-300 ease-in-out relative
                ${baseClasses}
                ${isActive ? '!scale-[1.05] !z-10 !shadow-[0_10px_25px_rgba(0,0,0,0.2)] !border-emerald-500 !bg-white/20 !border-white/40 !shadow-[0_0_20px_rgba(255,255,255,0.2)]' : 'hover:scale-[1.02] hover:bg-white/10'}
                ${isBlinking ? 'animate-click-blink' : ''}
            `}
        >
            <div className={isActive ? 'text-white font-semibold [&_*]:text-white [&_*]:font-semibold' : ''}>
                {children}
            </div>
        </div>
    );
};

export default Dashboard;

