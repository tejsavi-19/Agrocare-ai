import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, Leaf, User, Activity, History as HistoryIcon, BarChart3 } from 'lucide-react';

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav className="glass-nav sticky top-0 z-50 transition-all duration-300">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-20">
                    <div className="flex items-center">
                        <Link to="/" className="flex-shrink-0 flex items-center group">
                            <div className="bg-white/10 p-2 rounded-lg mr-3 shadow-md border border-white/20 group-hover:bg-white/20 transition-all backdrop-blur-sm">
                                <Leaf className="h-6 w-6 text-emerald-300 drop-shadow-[0_0_8px_rgba(52,211,153,0.8)]" />
                            </div>
                            <span className="font-extrabold text-2xl text-white tracking-tight drop-shadow-md">
                                AgroCare<span className="text-emerald-400 drop-shadow-[0_0_8px_rgba(52,211,153,0.5)]">AI</span>
                            </span>
                        </Link>
                    </div>

                    <div className="flex items-center space-x-1 sm:space-x-4">
                        <Link
                            to="/"
                            className="text-gray-200 hover:text-white px-3 py-2 rounded-lg text-sm font-semibold transition-all hover:bg-white/10 hover:shadow-[0_0_15px_rgba(255,255,255,0.1)]"
                        >
                            Home
                        </Link>

                        {user ? (
                            <>
                                <Link
                                    to="/dashboard"
                                    className="text-gray-200 hover:text-white px-3 py-2 rounded-lg text-sm font-semibold transition-all hover:bg-white/10 flex items-center"
                                >
                                    <Activity className="h-4 w-4 mr-2" /> Dashboard
                                </Link>
                                <Link
                                    to="/history"
                                    className="text-gray-200 hover:text-white px-3 py-2 rounded-lg text-sm font-semibold transition-all hover:bg-white/10 flex items-center"
                                >
                                    <HistoryIcon className="h-4 w-4 mr-2" /> History
                                </Link>
                                <Link
                                    to="/stats"
                                    className="text-gray-200 hover:text-white px-3 py-2 rounded-lg text-sm font-semibold transition-all hover:bg-white/10 flex items-center"
                                >
                                    <BarChart3 className="h-4 w-4 mr-2" /> Stats
                                </Link>

                                <div className="h-8 w-px bg-white/20 mx-2 hidden sm:block"></div>

                                <div className="flex items-center bg-black/20 px-3 py-1.5 rounded-full border border-white/10 backdrop-blur-md">
                                    <div className="bg-white/10 p-1 rounded-full mr-2">
                                        <User className="h-4 w-4 text-emerald-300" />
                                    </div>
                                    <span className="text-sm font-bold text-gray-100 mr-4 hidden md:inline">{user.name}</span>
                                    <button
                                        onClick={handleLogout}
                                        className="text-gray-400 hover:text-red-400 transition-colors p-1 hover:drop-shadow-[0_0_8px_rgba(248,113,113,0.8)]"
                                        title="Logout"
                                    >
                                        <LogOut className="h-4 w-4" />
                                    </button>
                                </div>
                            </>
                        ) : (
                            <div className="flex items-center space-x-3">
                                <Link
                                    to="/login"
                                    className="text-white hover:text-emerald-300 px-4 py-2 rounded-lg text-sm font-bold transition-colors"
                                >
                                    Login
                                </Link>
                                <Link
                                    to="/signup"
                                    className="glass-button px-5 py-2.5"
                                >
                                    Get Started
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

