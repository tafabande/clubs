import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Users, Calendar, ArrowUpRight, Heart } from 'lucide-react';
import { Badge } from '@/components/ui';
import type { Organization, OrganizationType } from '@/types';

interface OrganizationCardProps {
  organization: Organization;
}

const typeColors: Record<OrganizationType, string> = {
  club: 'default',
  church: 'info',
  sports_team: 'success',
  activity: 'warning',
};

const typeLabels: Record<OrganizationType, string> = {
  club: 'Club',
  church: 'Church',
  sports_team: 'Sports Team',
  activity: 'Activity',
};

export const OrganizationCard: React.FC<OrganizationCardProps> = ({ organization }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/organizations/${organization.organization_type}/${organization.id}`);
  };

  return (
    <motion.div
      whileHover={{ y: -8, scale: 1.02 }}
      transition={{ type: 'spring', damping: 15, stiffness: 300 }}
      className="h-full"
    >
      <div 
        onClick={handleClick}
        className="glass dark:glass-dark p-6 rounded-3xl h-full cursor-pointer group relative overflow-hidden transition-all duration-300 border border-transparent hover:border-msu-gold/30 shadow-lg hover:shadow-2xl"
      >
        <div className="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
          <ArrowUpRight className="text-msu-gold" size={20} />
        </div>

        {/* Cover Photo */}
        {organization.cover_photo && (
          <div className="h-32 -mx-6 -mt-6 mb-6 overflow-hidden">
            <img
              src={organization.cover_photo}
              alt={organization.name}
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-msu-blue/40 to-transparent pointer-events-none" />
          </div>
        )}

        {/* Header */}
        <div className="flex items-start gap-5 mb-5 relative z-10">
          {organization.logo ? (
            <img
              src={organization.logo}
              alt={organization.name}
              className="w-16 h-16 rounded-2xl object-cover border-2 border-white/20 shadow-xl group-hover:rotate-6 transition-transform"
            />
          ) : (
            <div className="w-16 h-16 rounded-2xl bg-msu-gold/20 flex items-center justify-center border-2 border-msu-gold/20 shadow-xl group-hover:rotate-6 transition-transform">
              <span className="text-2xl font-black text-msu-gold uppercase">
                {organization.name.charAt(0)}
              </span>
            </div>
          )}

          <div className="flex-1 min-w-0">
            <h3 className="text-xl font-black mb-1 truncate text-slate-900 dark:text-white group-hover:text-msu-blue dark:group-hover:text-msu-gold transition-colors">{organization.name}</h3>
            <div className="flex gap-2">
              <Badge variant={typeColors[organization.organization_type as OrganizationType] as any}>
                {typeLabels[organization.organization_type as OrganizationType]}
              </Badge>
              {organization.is_member && <Badge variant="success">Member</Badge>}
            </div>
          </div>
        </div>

        {/* Description */}
        <p className="text-slate-500 dark:text-white/60 text-sm mb-6 line-clamp-2 font-medium leading-relaxed">
          {organization.description}
        </p>

        {/* Stats */}
        <div className="flex items-center gap-4 text-xs font-black uppercase tracking-widest text-slate-400 dark:text-white/30">
          <div className="flex items-center gap-1.5">
            <Users size={14} className="text-msu-gold" />
            <span>{organization.members_count}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Heart size={14} className="text-red-500" />
            <span>{organization.followers_count}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Calendar size={14} className="text-msu-blue" />
            <span>{organization.posts_count}</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default OrganizationCard;
