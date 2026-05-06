// Organization Card Component

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Calendar } from 'lucide-react';
import { Card, Badge } from '@/components/ui';
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
    navigate(`/organizations/${organization.id}`);
  };

  return (
    <Card hover onClick={handleClick}>
      {/* Cover Photo */}
      {organization.cover_photo && (
        <div className="h-32 -mx-6 -mt-6 mb-4 overflow-hidden rounded-t-2xl">
          <img
            src={organization.cover_photo}
            alt={organization.name}
            className="w-full h-full object-cover"
          />
        </div>
      )}

      {/* Header */}
      <div className="flex items-start gap-4 mb-4">
        {organization.logo ? (
          <img
            src={organization.logo}
            alt={organization.name}
            className="w-16 h-16 rounded-xl object-cover border-2 border-white/20"
          />
        ) : (
          <div className="w-16 h-16 rounded-xl bg-white/10 flex items-center justify-center border-2 border-white/20">
            <span className="text-2xl font-bold text-msu-gold">
              {organization.name.charAt(0)}
            </span>
          </div>
        )}

        <div className="flex-1 min-w-0">
          <h3 className="text-xl font-bold mb-1 truncate">{organization.name}</h3>
          <Badge variant={typeColors[organization.organization_type] as any}>
            {typeLabels[organization.organization_type]}
          </Badge>
        </div>
      </div>

      {/* Description */}
      <p className="text-white/60 text-sm mb-4 line-clamp-2">
        {organization.description}
      </p>

      {/* Stats */}
      <div className="flex items-center gap-4 text-sm text-white/40">
        <div className="flex items-center gap-1">
          <Users size={16} />
          <span>{organization.members_count} members</span>
        </div>
        <div className="flex items-center gap-1">
          <Calendar size={16} />
          <span>{organization.posts_count} posts</span>
        </div>
      </div>

      {/* Member Badge */}
      {organization.is_member && (
        <div className="mt-4 pt-4 border-t border-white/10">
          <Badge variant="success">Member</Badge>
        </div>
      )}
    </Card>
  );
};

export default OrganizationCard;
