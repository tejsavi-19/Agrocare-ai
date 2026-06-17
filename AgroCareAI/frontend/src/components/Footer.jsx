import React from 'react';
import { Leaf, Github, Linkedin, Mail } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="bg-gray-900 text-white pt-12 pb-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                    <div className="col-span-1 md:col-span-2">
                        <div className="flex items-center mb-4">
                            <Leaf className="h-8 w-8 text-green-500 mr-2" />
                            <span className="font-bold text-2xl tracking-tight">AgroCare-AI</span>
                        </div>
                        <p className="text-gray-400 max-w-sm">
                            Empowering farmers and agricultural enthusiasts with AI-driven plant disease detection.
                            Upload an image and get instant, accurate diagnosis to protect your crops.
                        </p>
                    </div>

                    <div>
                        <h3 className="text-lg font-semibold mb-4 text-green-400">Quick Links</h3>
                        <ul className="space-y-2">
                            <li><a href="/" className="text-gray-400 hover:text-white transition-colors">Home</a></li>
                            <li><a href="/about" className="text-gray-400 hover:text-white transition-colors">About Us</a></li>
                            <li><a href="/dashboard" className="text-gray-400 hover:text-white transition-colors">Diagnose</a></li>
                            <li><a href="/stats" className="text-gray-400 hover:text-white transition-colors">Statistics</a></li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="text-lg font-semibold mb-4 text-green-400">Connect</h3>
                        <div className="flex space-x-4">
                            <a href="#" className="text-gray-400 hover:text-white transition-colors">
                                <Github className="h-6 w-6" />
                            </a>
                            <a href="#" className="text-gray-400 hover:text-white transition-colors">
                                <Linkedin className="h-6 w-6" />
                            </a>
                            <a href="mailto:contact@agrocare.ai" className="text-gray-400 hover:text-white transition-colors">
                                <Mail className="h-6 w-6" />
                            </a>
                        </div>
                    </div>
                </div>

                <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
                    <p className="text-gray-500 text-sm">
                        &copy; {new Date().getFullYear()} AgroCare-AI. All rights reserved.
                    </p>
                    <p className="text-gray-500 text-sm mt-2 md:mt-0">
                        Designed for Academic Project
                    </p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
