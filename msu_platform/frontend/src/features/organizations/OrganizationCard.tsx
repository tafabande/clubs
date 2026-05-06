import React from 'react';
import { Organization } from '@/types';
import { Button } from '@/components/ui/Button';

interface OrganizationCardProps {
  organization: Organization;
}

const OrganizationCard: React.FC<OrganizationCardProps> = ({ organization }) => {
  return (
    <div className="overflow-hidden rounded-lg border bg-white shadow-sm transition-shadow hover:shadow-md">
      {organization.cover_photo && (
        <img
          src={organization.cover_photo}
          alt={organization.name}
          className="h-32 w-full object-cover"
        />
      )}
      <div className="p-4">
        <div className="flex items-center space-x-3">
          {organization.logo && (
            <img
              src={organization.logo}
              alt={organization.name}
              className="h-12 w-12 rounded-full border bg-white object-contain"
            />
          )}
          <div>
            <h3 className="font-bold text-gray-900">{organization.name}</h3>
            <p className="text-xs text-gray-500 uppercase tracking-wider">
              {organization.organization_type}
            </p>
          </div>
        </div>
        <p className="mt-3 line-clamp-2 text-sm text-gray-600">
          {organization.description}
        </p>
        <div className="mt-4 flex items-center justify-between">
          <span className="text-sm text-gray-500">
            {organization.members_count} members
          </span>
          <Button variant="outline" size="sm">
            View Details
          </Button>
        </div>
      </div>
    </div>
  );
};

export default OrganizationCard;
