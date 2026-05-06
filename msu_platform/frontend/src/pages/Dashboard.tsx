// Dashboard Page - Role-Aware Router
// Automatically routes users to the correct dashboard based on their role.
// General users see their personal dashboard here.

import React from 'react';
import { Layout } from '@/components/layout';
import { Card, Spinner } from '@/components/ui';
import { PostCard, CreatePostWidget } from '@/components/features';
import { useInfinitePosts } from '@/hooks';
import { useAuth } from '@/hooks';
import { useRoles } from '@/hooks/useRoles';
import { Navigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/api';
import { API_ENDPOINTS, QUERY_KEYS } from '@/utils/constants';

const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const { dashboard, isLoading: roleLoading } = useRoles();

  // Redirect admin/mod/org_leader to their specific dashboards
  if (!roleLoading && dashboard === 'admin') return <Navigate to="/admin" replace />;
  if (!roleLoading && dashboard === 'moderator') return <Navigate to="/moderator" replace />;
  if (!roleLoading && dashboard === 'org_leader') return <Navigate to="/org-leader" replace />;

  const { data: userData, isLoading: userLoading } = useQuery({
    queryKey: [QUERY_KEYS.DASHBOARD_USER],
    queryFn: async () => {
      const res = await apiClient.get(API_ENDPOINTS.DASHBOARD_USER);
      return res.data;
    },
  });

  const { data, isLoading, error, hasNextPage, fetchNextPage, isFetchingNextPage } =
    useInfinitePosts({ ordering: '-created_at' });

  const posts = data?.pages.flatMap((page) => page.results) || [];

  if (roleLoading) {
    return <Layout><div className="flex justify-center py-32"><Spinner size="lg" /></div></Layout>;
  }

  return (
    <Layout>
      <div className="px-6 max-w-7xl mx-auto animate-in">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-black mb-2">
            Welcome back, {user?.first_name}!
          </h1>
          <p className="text-white/60">Stay updated with your organizations</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Feed */}
          <div className="lg:col-span-2 space-y-6">
            <CreatePostWidget />

            {isLoading && (
              <div className="flex justify-center py-20">
                <Spinner size="lg" />
              </div>
            )}

            {error && (
              <Card>
                <p className="text-red-400">Failed to load posts. Please try again.</p>
              </Card>
            )}

            {posts.length === 0 && !isLoading && (
              <Card>
                <p className="text-white/60 text-center py-10">
                  No posts yet. Join some organizations to see their updates!
                </p>
              </Card>
            )}

            {posts.map((post) => (
              <PostCard key={post.id} post={post} />
            ))}

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
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Profile Card */}
            <div className="glass-dark rounded-2xl p-6">
              <h3 className="font-bold mb-4 text-msu-gold">Your Profile</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between"><span className="text-white/50">Faculty</span><span className="text-white/80">{userData?.profile?.faculty || '-'}</span></div>
                <div className="flex justify-between"><span className="text-white/50">Department</span><span className="text-white/80">{userData?.profile?.department || '-'}</span></div>
                <div className="flex justify-between"><span className="text-white/50">Year</span><span className="text-white/80">{userData?.profile?.year || '-'}</span></div>
              </div>
            </div>

            {/* Stats */}
            <div className="glass-dark rounded-2xl p-6">
              <h3 className="font-bold mb-4 text-msu-gold">Your Stats</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-white/60">Organizations</span>
                  <span className="font-bold text-msu-gold">{userData?.stats?.organizations_joined || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white/60">Posts</span>
                  <span className="font-bold text-msu-gold">{userData?.stats?.posts_count || posts.length}</span>
                </div>
              </div>
            </div>

            {/* Memberships */}
            {userData?.memberships && (
              <div className="glass-dark rounded-2xl p-6">
                <h3 className="font-bold mb-4 text-msu-gold">Your Communities</h3>
                <div className="space-y-2">
                  {userData.memberships.clubs?.map((m: any) => (
                    <div key={m.id} className="flex items-center gap-2 text-sm bg-white/5 rounded-lg p-2">
                      <span>&#x1F3DB;</span>
                      <span className="text-white/80">{m.name}</span>
                      <span className="text-white/30 text-xs ml-auto">{m.position}</span>
                    </div>
                  ))}
                  {userData.memberships.churches?.map((m: any) => (
                    <div key={m.id} className="flex items-center gap-2 text-sm bg-white/5 rounded-lg p-2">
                      <span>&#x26EA;</span>
                      <span className="text-white/80">{m.name}</span>
                      <span className="text-white/30 text-xs ml-auto">{m.ministry}</span>
                    </div>
                  ))}
                  {userData.memberships.sports_teams?.map((m: any) => (
                    <div key={m.id} className="flex items-center gap-2 text-sm bg-white/5 rounded-lg p-2">
                      <span>&#x26BD;</span>
                      <span className="text-white/80">{m.name}</span>
                      <span className="text-white/30 text-xs ml-auto">{m.position}</span>
                    </div>
                  ))}
                  {(!userData.memberships.clubs?.length && !userData.memberships.churches?.length && !userData.memberships.sports_teams?.length) && (
                    <p className="text-white/30 text-sm text-center py-2">No communities joined yet</p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default DashboardPage;
