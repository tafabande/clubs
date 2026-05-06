import { motion, AnimatePresence } from 'framer-motion';
import { Search, Filter, Sparkles } from 'lucide-react';
import { Layout } from '@/components/layout';
import { Card, Spinner, Input, Badge } from '@/components/ui';
import { OrganizationCard } from '@/components/features';
import { useInfiniteOrganizations } from '@/hooks';
import type { OrganizationType } from '@/types';

const organizationTypes: { value: OrganizationType | 'all'; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'club', label: 'Clubs' },
  { value: 'church', label: 'Churches' },
  { value: 'sports_team', label: 'Sports Teams' },
  { value: 'activity', label: 'Activities' },
];

const OrganizationsPage: React.FC = () => {
  const [search, setSearch] = useState('');
  const [selectedType, setSelectedType] = useState<OrganizationType | 'all'>('all');

  const filters = {
    search: search.length > 2 ? search : undefined,
    organization_type: selectedType !== 'all' ? selectedType : undefined,
  };

  const { data, isLoading, error, hasNextPage, fetchNextPage, isFetchingNextPage } =
    useInfiniteOrganizations(filters);

  const organizations = data?.pages.flatMap((page) => page.results) || [];

  return (
    <Layout>
      <div className="px-6 max-w-7xl mx-auto pb-20">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="mb-12"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 glass dark:glass-dark text-msu-gold rounded-full text-xs font-black mb-4 uppercase tracking-widest">
            <Sparkles size={14} />
            Explore Community
          </div>
          <h1 className="text-5xl md:text-7xl font-black mb-4 tracking-tighter">
            DISCOVER <span className="text-gradient">ORGANIZATIONS</span>
          </h1>
          <p className="text-slate-500 dark:text-white/50 text-lg max-w-2xl font-medium">
            Join the most vibrant student communities at MSU. From academic clubs to sports teams, 
            find where you belong.
          </p>
        </motion.div>

        {/* Filters */}
        <div className="mb-12 grid lg:grid-cols-[1fr_auto] gap-6 items-end">
          <div className="space-y-4">
            <label className="text-xs font-black uppercase tracking-widest text-slate-400 dark:text-white/30 ml-1">Search & Discover</label>
            <div className="relative group">
              <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-msu-gold transition-colors" size={20} />
              <input
                type="text"
                placeholder="Search by name, category or keywords..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-14 pr-6 py-4 bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl focus:outline-none focus:ring-4 focus:ring-msu-gold/20 transition-all font-medium text-lg placeholder:text-slate-300 dark:placeholder:text-white/20 shadow-sm"
              />
            </div>
          </div>

          <div className="space-y-4">
            <label className="text-xs font-black uppercase tracking-widest text-slate-400 dark:text-white/30 ml-1 flex items-center gap-2">
              <Filter size={14} /> Filter by Type
            </label>
            <div className="flex flex-wrap gap-3">
              {organizationTypes.map((type) => (
                <motion.button
                  key={type.value}
                  whileHover={{ y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setSelectedType(type.value)}
                  className={`px-6 py-3 rounded-2xl font-black text-sm transition-all shadow-md ${
                    selectedType === type.value
                      ? 'bg-msu-gold text-msu-blue shadow-msu-gold/20'
                      : 'bg-white dark:bg-white/5 text-slate-600 dark:text-white/60 hover:bg-slate-50 dark:hover:bg-white/10 border border-slate-100 dark:border-white/5'
                  }`}
                >
                  {type.label}
                </motion.button>
              ))}
            </div>
          </div>
        </div>

        {/* Organizations Grid */}
        <AnimatePresence mode="popLayout">
          {isLoading ? (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center py-32"
            >
              <div className="w-16 h-16 border-4 border-msu-gold/20 border-t-msu-gold rounded-full animate-spin mb-6" />
              <p className="font-black text-slate-400 uppercase tracking-widest text-sm">Searching for tripes...</p>
            </motion.div>
          ) : organizations.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass dark:glass-dark p-20 rounded-[40px] text-center border-2 border-dashed border-slate-200 dark:border-white/10"
            >
              <div className="w-20 h-20 bg-slate-100 dark:bg-white/5 rounded-full flex items-center justify-center mx-auto mb-6">
                <Search size={40} className="text-slate-300 dark:text-white/20" />
              </div>
              <h3 className="text-2xl font-black mb-2">No organizations found</h3>
              <p className="text-slate-500 dark:text-white/40 font-medium">Try adjusting your filters or search terms.</p>
            </motion.div>
          ) : (
            <motion.div 
              layout
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
            >
              {organizations.map((org, index) => (
                <OrganizationCard key={org.id} organization={org} />
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {hasNextPage && !isLoading && (
          <div className="flex justify-center mt-16">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => fetchNextPage()}
              disabled={isFetchingNextPage}
              className="px-12 py-4 bg-msu-blue dark:bg-white/10 text-white font-black rounded-2xl shadow-xl shadow-msu-blue/20 hover:shadow-msu-blue/40 transition-all disabled:opacity-50"
            >
              {isFetchingNextPage ? 'Loading more...' : 'Load More Organizations'}
            </motion.button>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default OrganizationsPage;
