// Organizations Page Component

import React, { useState } from 'react';
import { Search } from 'lucide-react';
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
      <div className="px-6 max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-black mb-2">Discover Organizations</h1>
          <p className="text-white/60">Find and join clubs, churches, sports teams, and activities</p>
        </div>

        {/* Filters */}
        <div className="mb-8 space-y-4">
          {/* Search */}
          <div className="relative max-w-md">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40" size={20} />
            <Input
              type="text"
              placeholder="Search organizations..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-12"
            />
          </div>

          {/* Type Filter */}
          <div className="flex flex-wrap gap-2">
            {organizationTypes.map((type) => (
              <button
                key={type.value}
                onClick={() => setSelectedType(type.value)}
                className={`px-4 py-2 rounded-xl font-bold transition-colors ${
                  selectedType === type.value
                    ? 'bg-msu-gold text-msu-blue'
                    : 'bg-white/5 hover:bg-white/10'
                }`}
              >
                {type.label}
              </button>
            ))}
          </div>
        </div>

        {/* Organizations Grid */}
        {isLoading && (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        )}

        {error && (
          <Card>
            <p className="text-red-400">Failed to load organizations. Please try again.</p>
          </Card>
        )}

        {organizations.length === 0 && !isLoading && (
          <Card>
            <p className="text-white/60 text-center py-10">
              No organizations found. Try adjusting your filters.
            </p>
          </Card>
        )}

        {organizations.length > 0 && (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {organizations.map((org) => (
                <OrganizationCard key={org.id} organization={org} />
              ))}
            </div>

            {hasNextPage && (
              <div className="flex justify-center py-4">
                <button
                  onClick={() => fetchNextPage()}
                  disabled={isFetchingNextPage}
                  className="btn-secondary"
                >
                  {isFetchingNextPage ? 'Loading...' : 'Load More'}
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </Layout>
  );
};

export default OrganizationsPage;
