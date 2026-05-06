// Footer Component

import React from 'react';
import { Link } from 'react-router-dom';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-white/5 py-10 px-6 mt-20">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-msu-gold rounded-lg flex items-center justify-center">
                <span className="text-msu-blue font-black text-lg">M</span>
              </div>
              <span className="text-xl font-black">
                MSU<span className="text-msu-gold">HUB</span>
              </span>
            </div>
            <p className="text-white/40 text-sm">
              The official social platform for Midlands State University
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-white/60 text-sm">
              <li>
                <Link to="/organizations" className="hover:text-msu-gold transition-colors">
                  Organizations
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="hover:text-msu-gold transition-colors">
                  Dashboard
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="font-bold mb-4">Support</h3>
            <ul className="space-y-2 text-white/60 text-sm">
              <li>
                <a href="#" className="hover:text-msu-gold transition-colors">
                  Help Center
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-msu-gold transition-colors">
                  Contact Us
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="font-bold mb-4">Legal</h3>
            <ul className="space-y-2 text-white/60 text-sm">
              <li>
                <a href="#" className="hover:text-msu-gold transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-msu-gold transition-colors">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-white/5 pt-8 text-center text-white/30 text-sm">
          <p>&copy; 2026 MSU Hub Platform. Built with care for Midlands State University.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
