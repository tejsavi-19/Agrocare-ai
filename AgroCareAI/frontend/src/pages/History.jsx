import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Loader2, Calendar, AlertTriangle, CheckCircle, Clock, FileText } from 'lucide-react';

const History = () => {
    const [scans, setScans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedScan, setSelectedScan] = useState(null);
    const [loadingReport, setLoadingReport] = useState(false);
    const [activeCard, setActiveCard] = useState(null);

    const handleScanClick = async (scan) => {
        setSelectedScan(scan); // Show basic info immediately
        setLoadingReport(true);
        try {
            const response = await api.get(`/history/${scan.id}/report`);
            setSelectedScan(response.data);
        } catch (err) {
            console.error("Failed to load detailed report", err);
        } finally {
            setLoadingReport(false);
        }
    };

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await api.get('/history');
                setScans(response.data);
            } catch (err) {
                setError("Failed to fetch scan history.");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, []);

    if (loading) return (
        <div className="flex justify-center items-center h-screen bg-gray-50">
            <Loader2 className="animate-spin h-10 w-10 text-green-600" />
        </div>
    );

    return (
        <>
            <div className="min-h-screen text-gray-100 py-10 px-4 sm:px-6 lg:px-8">
                <div className="max-w-6xl mx-auto">
                    <div className="flex items-center justify-between mb-8">
                        <h1 className="text-3xl font-bold text-white">Scan History</h1>
                        <div className="bg-white px-4 py-2 rounded-lg shadow-sm text-sm text-green-900 border border-gray-100 italic">
                            Showing all past diagnoses
                        </div>
                    </div>

                    {error ? (
                        <div className="bg-red-50 p-4 rounded-xl border border-red-100 text-red-700 font-medium">
                            {error}
                        </div>
                    ) : scans.length === 0 ? (
                        <div className="glass-panel p-12 text-center text-white">
                            <Clock className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                            <h3 className="text-lg font-bold text-white">No scans found</h3>
                            <p className="text-emerald-100/70 mt-2 italic">Start by performing a diagnosis in the Dashboard.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {scans.map((scan) => (
                                <div
                                    key={scan.id}
                                    onClick={() => handleScanClick(scan)}
                                    className="glass-panel overflow-hidden border-white/20 hover:bg-white/10 transition-all duration-300 transform hover:scale-105 cursor-pointer relative group"
                                >
                                    <div className="absolute inset-0 bg-green-500 opacity-0 group-hover:opacity-5 transition-opacity"></div>
                                    <div className="h-48 overflow-hidden bg-black/30">
                                        <img
                                            src={`http://localhost:5000/api/uploads/${scan.image_path}`}
                                            alt={scan.prediction}
                                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                            onError={(e) => { e.target.src = 'https://via.placeholder.com/400x300?text=Scan+Image+NotFound'; }}
                                        />
                                    </div>
                                    <div className="p-6">
                                        <div className="flex justify-between items-start mb-4">
                                            <div>
                                                <h3 className={`text-xl font-bold ${scan.prediction === 'Healthy' ? 'text-green-600' : 'text-red-600'}`}>
                                                    {scan.prediction}
                                                </h3>
                                                <p className="text-xs text-emerald-100/60 font-medium flex items-center mt-1">
                                                    <Calendar className="h-3 w-3 mr-1" />
                                                    {new Date(scan.timestamp).toLocaleDateString()}
                                                </p>
                                            </div>
                                            <div className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${scan.prediction === 'Healthy' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                                }`}>
                                                ID: #{scan.id}
                                            </div>
                                        </div>

                                        <div className="space-y-3">
                                            <div className="flex items-center text-sm font-medium text-gray-300 bg-white/10 p-2 rounded-lg border border-white/5">
                                                <span className="w-24">Confidence:</span>
                                                <span className="text-white">{(scan.confidence * 1).toFixed(1)}%</span>
                                            </div>
                                            <div className="flex items-center text-sm font-medium text-gray-300 bg-white/10 p-2 rounded-lg border border-white/5">
                                                <span className="w-24">Risk Level:</span>
                                                <span className={`px-2 py-0.5 rounded text-xs ${scan.risk_level === 'High' ? 'text-red-600 font-bold' :
                                                    scan.risk_level === 'Medium' ? 'text-amber-600 font-bold' :
                                                        'text-green-600 font-bold'
                                                    }`}>{scan.risk_level}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Scan Detail Modal */}
            {selectedScan && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-200" onClick={() => setSelectedScan(null)}>
                    <div className="bg-black/60 backdrop-blur-3xl border border-white/20 rounded-3xl shadow-[0_0_40px_rgba(0,0,0,0.8)] max-w-3xl w-full max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
                        <div className="sticky top-0 bg-black/40 backdrop-blur-xl px-8 py-5 border-b border-white/10 flex justify-between items-center z-10">
                            <h2 className="text-2xl font-extrabold text-white">Scan Report #{selectedScan.id}</h2>
                            <button onClick={() => setSelectedScan(null)} className="p-2 hover:bg-black/30 rounded-full transition-colors">
                                <svg className="w-6 h-6 text-emerald-100/70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                            </button>
                        </div>

                        <div className="p-8">
                            <div className="flex flex-col lg:flex-row gap-8">
                                <div className="lg:w-1/3 space-y-6">
                                    <div className="rounded-2xl overflow-hidden shadow-md">
                                        <img
                                            src={`http://localhost:5000/api/uploads/${selectedScan.image_path || selectedScan.image}`} // Fallback to avoid breaking
                                            alt={selectedScan.prediction}
                                            className="w-full h-auto object-cover"
                                            onError={(e) => { e.target.src = 'https://via.placeholder.com/400x300?text=Scan+Image+NotFound'; }}
                                        />
                                    </div>

                                    <div>
                                        <div className="text-xs font-bold uppercase tracking-wider text-emerald-100/60 mb-1">Diagnosis Result</div>
                                        <h3 className={`text-3xl font-extrabold ${selectedScan.prediction === 'Healthy' ? 'text-green-600' : 'text-red-600'}`}>
                                            {selectedScan.prediction}
                                        </h3>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="glass-panel bg-black/20 p-4 shadow-none border-white/10">
                                            <div className="text-xs text-emerald-100/70 font-bold mb-1">Confidence Score</div>
                                            <div className="text-xl font-black text-white">{(selectedScan.confidence * 1).toFixed(1)}%</div>
                                        </div>
                                        <div className={`p-4 rounded-xl border ${selectedScan.risk_level === 'High' ? 'bg-red-500/20 border-red-400/30 text-red-100 text-red-300 drop-shadow-md' : selectedScan.risk_level === 'Medium' ? 'bg-amber-500/20 border-amber-400/30 text-amber-100 text-amber-900' : 'bg-emerald-500/20 border-emerald-400/30 text-emerald-100 text-green-900'}`}>
                                            <div className="text-xs font-bold mb-1 opacity-70">Risk Level</div>
                                            <div className="text-xl font-black">{selectedScan.risk_level}</div>
                                        </div>
                                    </div>

                                    <div className="bg-white p-5 rounded-xl border-2 border-gray-100 shadow-sm">
                                        <div className="text-sm font-bold text-gray-800 flex items-center gap-2 mb-2">
                                            <AlertTriangle className="h-4 w-4 text-amber-500" /> System Advice
                                        </div>
                                        <p className="text-sm text-gray-300 leading-relaxed font-medium">
                                            {selectedScan.advice}
                                        </p>
                                    </div>
                                </div>

                                <div className="lg:w-2/3">
                                    {loadingReport ? (
                                        <div className="flex flex-col items-center justify-center h-full space-y-4">
                                            <Loader2 className="h-8 w-8 text-green-600 animate-spin" />
                                            <p className="text-sm font-bold text-emerald-100/70">Generating detailed Knowledge Base report...</p>
                                        </div>
                                    ) : selectedScan.knowledge_base && typeof selectedScan.knowledge_base === 'object' ? (
                                        <div className="space-y-4">
                                            <p className="text-[10px] font-black text-emerald-100/60 uppercase tracking-widest flex items-center gap-2 border-b pb-2">
                                                <FileText className="h-3 w-3" /> Detailed Analysis Report
                                            </p>

                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="desc" baseClasses="glass-panel p-4">
                                                    <h4 className="font-bold text-slate-800 text-sm mb-1 flex items-center gap-2">📝 Description</h4>
                                                    <p className="text-xs text-gray-300">{selectedScan.description}</p>
                                                </InteractiveCard>

                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="what" baseClasses="glass-panel p-4">
                                                    <h4 className="font-bold text-slate-800 text-sm mb-1 flex items-center gap-2">🔍 What is it?</h4>
                                                    <p className="text-xs text-gray-300">{selectedScan.knowledge_base.detailed_explanation?.what_is_it || "Information not found."}</p>
                                                </InteractiveCard>
                                            </div>

                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="risk" baseClasses="glass-panel bg-red-500/10 p-4 border-red-400/30">
                                                    <h4 className="font-bold text-red-300 drop-shadow-md text-sm mb-2 flex items-center gap-2">🚨 Severity & Risk</h4>
                                                    <div className="text-xs text-red-800 space-y-1 mt-3">
                                                        <p><strong>System Risk Score:</strong> {selectedScan.confidence?.toFixed(1)}%</p>
                                                        <p><strong>Disease Severity:</strong> {selectedScan.knowledge_base.severity_level || "Unknown"}</p>
                                                        <p><strong>Spread Velocity:</strong> {selectedScan.knowledge_base.spread_risk || "Unknown"}</p>
                                                    </div>
                                                </InteractiveCard>

                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="symptoms" baseClasses="glass-panel bg-amber-500/10 p-4 border-amber-400/30">
                                                    <h4 className="font-bold text-amber-900 text-sm mb-2 flex items-center gap-2">⚠️ Symptoms</h4>
                                                    <div className="text-xs text-amber-800 space-y-2">
                                                        {selectedScan.knowledge_base.symptoms ? (
                                                            <>
                                                                {selectedScan.knowledge_base.symptoms.leaf_symptoms && <p><strong>Leaves:</strong> {selectedScan.knowledge_base.symptoms.leaf_symptoms}</p>}
                                                                {selectedScan.knowledge_base.symptoms.stem_symptoms && <p><strong>Stem:</strong> {selectedScan.knowledge_base.symptoms.stem_symptoms}</p>}
                                                                {selectedScan.knowledge_base.symptoms.fruit_symptoms && <p><strong>Fruit:</strong> {selectedScan.knowledge_base.symptoms.fruit_symptoms}</p>}
                                                            </>
                                                        ) : (
                                                            <p>Symptoms information unavailable.</p>
                                                        )}
                                                    </div>
                                                </InteractiveCard>
                                            </div>

                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="causes" baseClasses="glass-panel p-4">
                                                    <h4 className="font-bold text-slate-800 text-sm mb-2 flex items-center gap-2">🧬 Causes</h4>
                                                    <p className="text-xs text-gray-300 mb-1">{selectedScan.knowledge_base.causes?.biological_or_environmental || "Information not found."}</p>
                                                    {selectedScan.knowledge_base.causes?.weather_conditions && (
                                                        <p className="text-xs text-gray-300 mb-1"><strong>Weather:</strong> {selectedScan.knowledge_base.causes.weather_conditions}</p>
                                                    )}
                                                </InteractiveCard>

                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="prevention" baseClasses="glass-panel p-4">
                                                    <h4 className="font-bold text-slate-800 text-sm mb-2 flex items-center gap-2">🛡️ Precautions & Prevention</h4>
                                                    {selectedScan.precautions && selectedScan.precautions.length > 0 ? (
                                                        <ul className="text-xs text-gray-300 list-disc ml-4 space-y-1">
                                                            {selectedScan.precautions.map((prec, idx) => (
                                                                <li key={idx}>{prec}</li>
                                                            ))}
                                                        </ul>
                                                    ) : (
                                                        <p className="text-xs text-gray-300 italic">No specific precautions available.</p>
                                                    )}
                                                </InteractiveCard>
                                            </div>

                                            {selectedScan.knowledge_base.is_critical ? (
                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="treatment" baseClasses="glass-panel bg-red-500/20 p-5 border-red-400/50 shadow-[0_0_15px_rgba(248,113,113,0.2)] mt-4">
                                                    <h4 className="font-bold text-red-300 drop-shadow-md text-lg mb-2 flex items-center gap-2">❌ Plant Not Suitable</h4>
                                                    <p className="text-sm text-red-800 font-medium">⚠️ This plant is not suitable to keep. There is no solution to cure it at this stage. Please remove and destroy this plant immediately.</p>
                                                </InteractiveCard>
                                            ) : (
                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="treatment" baseClasses="glass-panel bg-emerald-500/10 p-5 border-emerald-400/30 mt-4">
                                                    <h4 className="font-bold text-emerald-300 drop-shadow-md text-sm mb-3 flex items-center gap-2">💊 Treatment Steps</h4>
                                                    {selectedScan.treatment && selectedScan.treatment.length > 0 ? (
                                                        <ul className="text-xs text-emerald-700 list-disc ml-4 space-y-1">
                                                            {selectedScan.treatment.map((treat, idx) => (
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

                                            {selectedScan.knowledge_base.additional_farmer_tips && (
                                                <InteractiveCard activeCard={activeCard} setActiveCard={setActiveCard} id="tips" baseClasses="glass-panel bg-indigo-500/10 p-4 border-indigo-400/30 mt-4">
                                                    <h4 className="font-bold text-indigo-900 text-sm mb-1 flex items-center gap-2">🧑‍🌾 Farmer Tip</h4>
                                                    <p className="text-xs text-indigo-800 italic">{selectedScan.knowledge_base.additional_farmer_tips}</p>
                                                </InteractiveCard>
                                            )}
                                        </div>
                                    ) : (
                                        <div className="flex flex-col items-center justify-center h-full glass-panel bg-black/20 border-2 border-dashed border-white/10 p-6">
                                            <FileText className="h-10 w-10 text-gray-300 mb-2" />
                                            <p className="text-emerald-100/70 font-medium">{selectedScan.prediction === 'Healthy' ? "Healthy plant lacks a detailed disease report." : "Detailed knowledge base report unavailable for this scan."}</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

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

export default History;
