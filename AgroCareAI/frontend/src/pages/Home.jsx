import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2, ShieldCheck, BrainCircuit, Sprout, Microscope } from 'lucide-react';

const Home = () => {
    return (
        <div className="flex flex-col min-h-screen font-sans selection:bg-emerald-400 selection:text-black text-gray-100">
            {/* Hero Section */}
            <section className="relative pt-24 pb-20 lg:pt-32 lg:pb-40 overflow-hidden">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
                    <div className="flex flex-col lg:flex-row items-center gap-16">
                        <div className="lg:w-1/2">
                            <div className="glass-badge inline-flex items-center px-4 py-1.5 rounded-full text-xs uppercase tracking-widest mb-6">
                                <span className="flex h-2 w-2 rounded-full bg-emerald-400 mr-2 animate-pulse"></span>
                                Precision Agriculture AI
                            </div>
                            <h1 className="text-5xl lg:text-7xl font-extrabold text-white leading-[1.1] mb-8 drop-shadow-md">
                                Advanced <span className="text-emerald-400 drop-shadow-[0_0_12px_rgba(52,211,153,0.5)]">Plant Health</span> Diagnostics
                            </h1>
                            <p className="text-xl text-emerald-50/80 mb-10 leading-relaxed max-w-xl">
                                Leverage state-of-the-art computer vision to secure your crops.
                                Get instant, lab-grade disease analysis from a single photograph.
                            </p>
                            <div className="flex flex-col sm:flex-row gap-5">
                                <Link to="/dashboard" className="glass-button py-4 px-10 flex items-center justify-center text-lg">
                                    Start Diagnosis <ArrowRight className="ml-2 h-5 w-5" />
                                </Link>
                                <Link to="/signup" className="glass-panel hover:bg-white/10 text-white font-bold py-4 px-10 rounded-xl transition-all flex items-center justify-center text-lg shadow-none">
                                    Join Network
                                </Link>
                            </div>

                            <div className="mt-12 flex items-center gap-8 text-gray-300">
                                <div className="flex flex-col">
                                    <span className="text-2xl font-bold text-white drop-shadow-sm">96.8%</span>
                                    <span className="text-xs uppercase font-bold tracking-tighter text-emerald-300/70">Model Accuracy</span>
                                </div>
                                <div className="h-10 w-px bg-white/20"></div>
                                <div className="flex flex-col">
                                    <span className="text-2xl font-bold text-white drop-shadow-sm">2s</span>
                                    <span className="text-xs uppercase font-bold tracking-tighter text-emerald-300/70">Response Time</span>
                                </div>
                            </div>
                        </div>

                        <div className="lg:w-1/2 w-full">
                            <div className="relative">
                                <div className="absolute -inset-4 bg-emerald-400/20 rounded-[2.5rem] blur-2xl"></div>
                                <div className="relative rounded-[2rem] overflow-hidden glass-panel border border-white/30 group">
                                    <img
                                        src="https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?auto=format&fit=crop&w=2000&q=80"
                                        alt="High-resolution plant scan"
                                        className="w-full h-[500px] object-cover transition-transform duration-700 group-hover:scale-105 opacity-90"
                                    />
                                    <div className="absolute top-6 left-6 glass-panel p-4 !rounded-2xl border border-white/30">
                                        <div className="flex items-center gap-3">
                                            <div className="p-2 bg-emerald-500/30 rounded-lg backdrop-blur-sm border border-emerald-300/30">
                                                <Microscope className="h-5 w-5 text-emerald-300 drop-shadow-[0_0_8px_rgba(110,231,183,0.8)]" />
                                            </div>
                                            <div>
                                                <p className="text-[10px] font-bold text-emerald-100/70 uppercase tracking-widest drop-shadow">Scanning...</p>
                                                <p className="text-sm font-bold text-white drop-shadow-md">Leaf Tissues Analyzed</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="absolute bottom-6 right-6 bg-emerald-500/80 backdrop-blur-md p-4 rounded-2xl shadow-[0_0_15px_rgba(16,185,129,0.5)] border border-white/40 text-white">
                                        <CheckCircle2 className="h-8 w-8 drop-shadow-[0_0_8px_rgba(255,255,255,0.8)]" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-24 relative overflow-hidden">
                <div className="absolute inset-0 bg-black/40 backdrop-blur-md -z-10 border-y border-white/10"></div>
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-20">
                        <h2 className="text-sm font-bold text-emerald-400 uppercase tracking-[0.3em] mb-4 drop-shadow-[0_0_8px_rgba(52,211,153,0.8)]">Core Technology</h2>
                        <h3 className="text-4xl font-extrabold text-white mb-6 drop-shadow-md">Built for Agricultural Professionals</h3>
                        <p className="text-lg text-emerald-100/80 max-w-2xl mx-auto">
                            AgroCare-AI merges deep-learning models with botanical data to deliver
                            actionable insights directly to the hands of farmers and researchers.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                        <FeatureCard
                            icon={<BrainCircuit className="h-8 w-8 text-emerald-300 drop-shadow-[0_0_8px_rgba(110,231,183,0.8)]" />}
                            title="Neural Architecture"
                            desc="Optimized MobileNetV3 backbone capable of identifying complex disease patterns even in varying lighting conditions."
                        />
                        <FeatureCard
                            icon={<Sprout className="h-8 w-8 text-emerald-300 drop-shadow-[0_0_8px_rgba(110,231,183,0.8)]" />}
                            title="Full-Stack Diagnostics"
                            desc="Identify diseases across various crop families with categorical risk assessment and tailored chemical/organic advice."
                        />
                        <FeatureCard
                            icon={<ShieldCheck className="h-8 w-8 text-emerald-300 drop-shadow-[0_0_8px_rgba(110,231,183,0.8)]" />}
                            title="Bio-Security"
                            desc="Maintain a secure, timestamped record of every scan to monitor crop epidemiology throughout the growing season."
                        />
                    </div>
                </div>
            </section>

            {/* Steps Section */}
            <section className="py-24 relative">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-3xl font-extrabold text-white mb-16 drop-shadow-md">Simple. Effective. Instant.</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-16 relative">
                        <div className="absolute top-1/2 left-0 w-full h-px bg-white/20 hidden md:block -z-10"></div>
                        <StepItem num="1" title="Capture Image" text="Take a high-res photo of the leaf surface." />
                        <StepItem num="2" title="AI Validation" text="Model performs multi-layer feature extraction." />
                        <StepItem num="3" title="Apply Treatment" text="Receive instant remediation and risk advice." />
                    </div>
                </div>
            </section>
        </div>
    );
};

const FeatureCard = ({ icon, title, desc }) => (
    <div className="glass-panel p-10 group">
        <div className="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center mb-8 border border-white/20 group-hover:bg-white/20 transition-all backdrop-blur-md">
            {icon}
        </div>
        <h4 className="text-xl font-bold text-white mb-4 drop-shadow-sm">{title}</h4>
        <p className="text-emerald-50/70 leading-relaxed text-sm">
            {desc}
        </p>
    </div>
);

const StepItem = ({ num, title, text }) => (
    <div className="flex flex-col items-center">
        <div className="w-14 h-14 rounded-2xl bg-black/40 backdrop-blur-md border border-white/20 text-white flex items-center justify-center text-xl font-black mb-6 shadow-[0_0_15px_rgba(52,211,153,0.3)]">
            {num}
        </div>
        <h5 className="text-lg font-bold text-white mb-2 drop-shadow-sm">{title}</h5>
        <p className="text-emerald-100/70 text-sm">{text}</p>
    </div>
);

export default Home;

