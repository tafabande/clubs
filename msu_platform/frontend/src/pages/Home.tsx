// Home Page Component

import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Users,
  Search,
  Flame,
  MessageSquare,
  Calendar,
  Trophy,
  ChevronRight,
} from 'lucide-react';
import { motion } from 'framer-motion';
import { Layout } from '@/components/layout';
import { Button } from '@/components/ui';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { type: 'spring', damping: 20, stiffness: 100 }
    },
  };

  const floatAnimation = {
    y: [0, -15, 0],
    transition: {
      duration: 5,
      repeat: Infinity,
      ease: "easeInOut"
    }
  };

  return (
    <Layout>
      {/* Hero Section */}
      <section className="px-6 max-w-7xl mx-auto mb-24 min-h-[80vh] flex items-center">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={containerVariants}
          className="grid lg:grid-cols-2 gap-16 items-center w-full"
        >
          <div className="relative z-10">
            <motion.div
              variants={itemVariants}
              className="inline-flex items-center gap-2 px-5 py-2 glass dark:glass-dark text-msu-gold rounded-full text-sm font-black mb-8 tracking-wider uppercase"
            >
              <Flame size={16} className="animate-pulse" />
              Official MSU Student Hub
            </motion.div>
            <motion.h1
              variants={itemVariants}
              className="text-6xl md:text-8xl font-black leading-[0.9] mb-8 tracking-tighter"
            >
              CONNECT <br />
              <span className="text-gradient">EVERYWHERE</span>
            </motion.h1>
            <motion.p
              variants={itemVariants}
              className="text-xl text-slate-600 dark:text-white/60 mb-12 max-w-lg leading-relaxed font-medium"
            >
              The digital heartbeat of Midlands State University. Join clubs, 
              find your tribe, and experience campus life like never before.
            </motion.p>
            <motion.div variants={itemVariants} className="flex flex-wrap gap-6 items-center">
              <button 
                className="btn-gold px-10 py-4 text-lg group"
                onClick={() => navigate('/organizations')}
              >
                Start Exploring 
                <ChevronRight className="group-hover:translate-x-1 transition-transform" />
              </button>
              <div className="flex -space-x-3 items-center">
                {[1, 2, 3, 4].map((i) => (
                  <motion.div
                    key={i}
                    whileHover={{ y: -5, zIndex: 10 }}
                    className="w-12 h-12 rounded-full border-4 border-white dark:border-msu-dark bg-slate-200 overflow-hidden shadow-xl"
                  >
                    <img src={`https://i.pravatar.cc/150?u=msu${i}`} alt="Student" />
                  </motion.div>
                ))}
                <div className="pl-6">
                  <p className="text-sm font-black text-msu-blue dark:text-msu-gold">2.4k+ Active</p>
                  <p className="text-xs text-slate-400">Students joined today</p>
                </div>
              </div>
            </motion.div>
          </div>

          <motion.div 
            variants={itemVariants} 
            animate={floatAnimation}
            className="relative perspective-1000"
          >
            <div className="relative z-10 aspect-[4/3] glass dark:glass-dark rounded-3xl overflow-hidden shadow-[0_50px_100px_-20px_rgba(0,0,0,0.3)] rotate-2 hover:rotate-0 transition-all duration-700 cursor-pointer group">
              <div className="absolute inset-0 bg-gradient-to-br from-msu-blue/40 to-msu-gold/20 mix-blend-overlay group-hover:opacity-0 transition-opacity" />
              <div className="p-10 h-full flex flex-col justify-between relative z-10">
                <div className="flex justify-between items-start">
                  <div className="glass dark:glass-dark p-5 rounded-2xl shadow-inner">
                    <Trophy className="text-msu-gold" size={40} />
                  </div>
                  <div className="glass dark:glass-dark px-6 py-3 rounded-full text-sm font-black tracking-widest uppercase">
                    Live Feed
                  </div>
                </div>

                <div className="space-y-6">
                  <motion.div 
                    whileHover={{ scale: 1.05, x: 10 }}
                    className="glass dark:glass-dark p-6 flex items-center gap-5 rounded-2xl shadow-2xl border-l-4 border-msu-gold"
                  >
                    <div className="w-14 h-14 bg-msu-gold rounded-xl flex items-center justify-center text-msu-blue font-black">DR</div>
                    <div className="flex-1">
                      <div className="h-5 bg-slate-200 dark:bg-white/10 rounded-full w-2/3 mb-2" />
                      <div className="h-3 bg-slate-100 dark:bg-white/5 rounded-full w-1/2" />
                    </div>
                  </motion.div>
                  <motion.div 
                    whileHover={{ scale: 1.05, x: -10 }}
                    className="glass dark:glass-dark p-6 translate-x-12 flex items-center gap-5 rounded-2xl shadow-2xl border-l-4 border-msu-blue"
                  >
                    <div className="w-14 h-14 bg-msu-blue rounded-xl flex items-center justify-center text-white font-black">SC</div>
                    <div className="flex-1">
                      <div className="h-5 bg-slate-200 dark:bg-white/10 rounded-full w-3/4 mb-2" />
                      <div className="h-3 bg-slate-100 dark:bg-white/5 rounded-full w-1/3" />
                    </div>
                  </motion.div>
                </div>
              </div>
            </div>
            
            {/* 3D Decorative elements */}
            <div className="absolute -top-12 -right-12 w-64 h-64 bg-msu-gold/30 rounded-full blur-[100px] -z-10" />
            <div className="absolute -bottom-12 -left-12 w-80 h-80 bg-msu-blue/30 rounded-full blur-[120px] -z-10" />
          </motion.div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section className="px-6 max-w-7xl mx-auto pb-32">
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-black mb-4">Elevate Your <span className="text-msu-gold">Experience</span></h2>
          <p className="text-slate-500 dark:text-white/40 max-w-2xl mx-auto text-lg">Powerful features designed specifically for the MSU student community.</p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {[
            {
              icon: Users,
              title: 'Clubs & Socs',
              desc: 'Join academic, social and interest-based clubs.',
              color: 'text-blue-500'
            },
            {
              icon: Calendar,
              title: 'Campus Events',
              desc: 'Never miss an event on the Gweru campus.',
              color: 'text-msu-gold'
            },
            {
              icon: MessageSquare,
              title: 'Social Feed',
              desc: 'Share your moments with fellow students.',
              color: 'text-green-500'
            },
            { 
              icon: Search, 
              title: 'Fast Discovery', 
              desc: 'Find organizations using full-text search.',
              color: 'text-purple-500'
            },
          ].map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              whileHover={{ 
                y: -10, 
                rotateX: 5, 
                rotateY: 5,
                transition: { duration: 0.2 }
              }}
              className="glass dark:glass-dark p-8 rounded-3xl relative overflow-hidden group cursor-pointer shadow-lg hover:shadow-2xl transition-all"
            >
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-msu-gold/10 to-transparent rounded-bl-[100px] group-hover:scale-150 transition-transform duration-500" />
              
              <div className={`w-16 h-16 bg-slate-100 dark:bg-white/5 rounded-2xl flex items-center justify-center mb-8 group-hover:bg-msu-gold group-hover:text-msu-blue transition-all duration-300 shadow-inner ${feature.color}`}>
                <feature.icon size={32} />
              </div>
              <h3 className="text-2xl font-black mb-4 tracking-tight">{feature.title}</h3>
              <p className="text-slate-500 dark:text-white/40 leading-relaxed font-medium">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </Layout>
  );
};

export default HomePage;
