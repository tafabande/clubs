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
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5, staggerChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <Layout>
      {/* Hero Section */}
      <section className="px-6 max-w-7xl mx-auto mb-20">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={containerVariants}
          className="grid lg:grid-cols-2 gap-12 items-center"
        >
          <div>
            <motion.div
              variants={itemVariants}
              className="inline-flex items-center gap-2 px-4 py-2 glass text-msu-gold rounded-full text-sm font-bold mb-6"
            >
              <Flame size={16} />
              The Official Midlands State University Platform
            </motion.div>
            <motion.h1
              variants={itemVariants}
              className="text-6xl md:text-8xl font-black leading-none mb-6 tracking-tighter"
            >
              DISCOVER <br />
              <span className="text-msu-gold">YOUR TRIBE</span>
            </motion.h1>
            <motion.p
              variants={itemVariants}
              className="text-xl text-white/60 mb-10 max-w-lg leading-relaxed"
            >
              The all-in-one social platform for MSU organizations. Connect with clubs, churches,
              sports teams, and activities across the Gweru Campus.
            </motion.p>
            <motion.div variants={itemVariants} className="flex flex-wrap gap-4">
              <Button size="lg" onClick={() => navigate('/organizations')}>
                Explore Clubs <ChevronRight />
              </Button>
              <div className="flex -space-x-4 items-center pl-4">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="w-12 h-12 rounded-full border-4 border-msu-dark bg-white/10 overflow-hidden"
                  >
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
            <div className="absolute -top-10 -right-10 w-40 h-40 bg-msu-gold/20 rounded-full blur-3xl" />
            <div className="absolute -bottom-10 -left-10 w-60 h-60 bg-msu-blue/40 rounded-full blur-3xl" />
          </motion.div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section className="px-6 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              icon: Users,
              title: 'Clubs & Socs',
              desc: 'Join academic, social and interest-based clubs.',
            },
            {
              icon: Calendar,
              title: 'Campus Events',
              desc: 'Never miss an event on the Gweru campus.',
            },
            {
              icon: MessageSquare,
              title: 'Social Feed',
              desc: 'Share your moments with fellow students.',
            },
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
    </Layout>
  );
};

export default HomePage;
