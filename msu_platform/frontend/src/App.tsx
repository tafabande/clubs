import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Search, 
  Flame, 
  MessageSquare, 
  LayoutDashboard, 
  Calendar, 
  Trophy, 
  ChevronRight,
  LogOut,
  Bell,
  Plus
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activeTab, setActiveTab] = useState('home');

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.5, staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="glass fixed top-4 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl px-8 py-4 z-50 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-msu-gold rounded-lg flex items-center justify-center">
            <span className="text-msu-blue font-black text-xl">M</span>
          </div>
          <span className="text-2xl font-black tracking-tighter">
            MSU<span className="text-msu-gold">HUB</span>
          </span>
        </div>

        <div className="hidden md:flex items-center gap-8">
          <a href="#" className="hover:text-msu-gold transition-colors">Organizations</a>
          <a href="#" className="hover:text-msu-gold transition-colors">Social Feed</a>
          <a href="#" className="hover:text-msu-gold transition-colors">Events</a>
          <a href="#" className="hover:text-msu-gold transition-colors">About</a>
        </div>

        <div className="flex items-center gap-4">
          <button className="btn-secondary hidden sm:flex">Login</button>
          <button className="btn-primary">Join Now</button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-40 pb-20 px-6 max-w-7xl mx-auto">
        <motion.div 
          initial="hidden"
          animate="visible"
          variants={containerVariants}
          className="grid lg:grid-cols-2 gap-12 items-center"
        >
          <div>
            <motion.div variants={itemVariants} className="inline-flex items-center gap-2 px-4 py-2 glass text-msu-gold rounded-full text-sm font-bold mb-6">
              <Flame size={16} />
              The Official Midlands State University Platform
            </motion.div>
            <motion.h1 variants={itemVariants} className="text-6xl md:text-8xl font-black leading-none mb-6 tracking-tighter">
              DISCOVER <br />
              <span className="text-msu-gold">YOUR TRIBE</span>
            </motion.h1>
            <motion.p variants={itemVariants} className="text-xl text-white/60 mb-10 max-w-lg leading-relaxed">
              The all-in-one social platform for MSU organizations. Connect with clubs, churches, sports teams, and activities across the Gweru Campus.
            </motion.p>
            <motion.div variants={itemVariants} className="flex flex-wrap gap-4">
              <button className="btn-primary py-4 px-10 text-lg">
                Explore Clubs <ChevronRight />
              </button>
              <div className="flex -space-x-4 items-center pl-4">
                {[1,2,3,4].map(i => (
                  <div key={i} className="w-12 h-12 rounded-full border-4 border-msu-dark bg-white/10 overflow-hidden">
                    <img src={`https://i.pravatar.cc/150?u=${i}`} alt="Avatar" />
                  </div>
                ))}
                <span className="pl-6 text-white/60 font-medium">+2.4k students joined</span>
              </div>
            </motion.div>
          </div>

          <motion.div variants={itemVariants} className="relative">
            <div className="aspect-square glass overflow-hidden rotate-3 hover:rotate-0 transition-transform duration-700">
               <div className="absolute inset-0 bg-gradient-to-br from-msu-gold/20 to-transparent pointer-events-none" />
               <div className="p-8 h-full flex flex-col justify-between">
                  <div className="flex justify-between items-start">
                    <div className="glass p-4">
                      <Trophy className="text-msu-gold" size={32} />
                    </div>
                    <div className="glass px-4 py-2 text-sm font-bold">Trending #MSUDebate</div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="glass p-4 flex items-center gap-4">
                       <div className="w-12 h-12 bg-white/10 rounded-xl" />
                       <div className="flex-1">
                          <div className="h-4 bg-white/10 rounded w-2/3 mb-2" />
                          <div className="h-3 bg-white/5 rounded w-1/2" />
                       </div>
                    </div>
                    <div className="glass p-4 translate-x-12 flex items-center gap-4">
                       <div className="w-12 h-12 bg-msu-gold rounded-xl" />
                       <div className="flex-1">
                          <div className="h-4 bg-msu-blue/20 rounded w-3/4 mb-2" />
                          <div className="h-3 bg-msu-blue/10 rounded w-1/3" />
                       </div>
                    </div>
                  </div>
               </div>
            </div>
            {/* Decor */}
            <div className="absolute -top-10 -right-10 w-40 h-40 bg-msu-gold/20 rounded-full blur-3xl" />
            <div className="absolute -bottom-10 -left-10 w-60 h-60 bg-msu-blue/40 rounded-full blur-3xl" />
          </motion.div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            { icon: Users, title: 'Clubs & Socs', desc: 'Join academic, social and interest-based clubs.' },
            { icon: Calendar, title: 'Campus Events', desc: 'Never miss an event on the Gweru campus.' },
            { icon: MessageSquare, title: 'Social Feed', desc: 'Share your moments with fellow students.' },
            { icon: Search, title: 'Fast Discovery', desc: 'Find organizations using full-text search.' },
          ].map((feature, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="card group"
            >
              <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center mb-6 group-hover:bg-msu-gold group-hover:text-msu-blue transition-colors">
                <feature.icon size={24} />
              </div>
              <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
              <p className="text-white/50 leading-relaxed">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-10 px-6 text-center text-white/30 text-sm">
        <p>&copy; 2026 MSU Hub Platform. Built with ❤️ for Midlands State University.</p>
      </footer>
    </div>
  );
};

export default App;
