// Organization Leader Dashboard - Scoped to own organizations only
// Manage page, members, posts, events, view engagement stats

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Layout } from '@/components/layout';
import { Card, Spinner } from '@/components/ui';
import { apiClient } from '@/services/api';
import { API_ENDPOINTS, QUERY_KEYS } from '@/utils/constants';

const OrgLeaderDashboard: React.FC = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: [QUERY_KEYS.DASHBOARD_ORG_LEADER],
    queryFn: async () => {
      const res = await apiClient.get(API_ENDPOINTS.DASHBOARD_ORG_LEADER);
      return res.data;
    },
    refetchInterval: 30000,
  });

  if (isLoading) {
    return <Layout><div className="flex justify-center py-32"><Spinner size="lg" /></div></Layout>;
  }

  if (error || !data) {
    return <Layout><div className="max-w-7xl mx-auto px-6"><Card><p className="text-red-400">You don't lead any organizations.</p></Card></div></Layout>;
  }

  const orgTypeIcons: Record<string, string> = {
    club: '\u{1F3DB}', church: '\u{26EA}', sportsteam: '\u{26BD}', activity: '\u{1F4C5}',
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-6 animate-in">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">&#x1F451;</span>
            <h1 className="text-4xl font-black text-gradient">Your Organizations</h1>
          </div>
          <p className="text-white/50">Manage your organizations, members, and content.</p>
        </div>

        <div className="space-y-8">
          {data.organizations?.map((org: any) => (
            <div key={org.id} className="glass-dark rounded-2xl p-6 hover:border-msu-gold/30 border border-white/5 transition-all">
              {/* Org Header */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-4">
                  <span className="text-4xl">{orgTypeIcons[org.type] || '\u{1F3E2}'}</span>
                  <div>
                    <h2 className="text-xl font-black text-white">{org.name}</h2>
                    <div className="flex items-center gap-3 text-sm">
                      <span className="text-msu-gold font-semibold">{org.role}</span>
                      <span className="text-white/30">|</span>
                      <span className="text-white/50 capitalize">{org.type}</span>
                    </div>
                  </div>
                </div>
                <a
                  href={`/organizations/${org.type}/${org.id}`}
                  className="btn-gold text-sm !py-2 !px-4 !rounded-xl"
                >
                  View Page
                </a>
              </div>

              {/* Org Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-white/5 rounded-xl p-4 text-center">
                  <div className="text-2xl font-black text-msu-gold">{org.members_count}</div>
                  <div className="text-white/50 text-xs">Members</div>
                </div>
                <div className="bg-white/5 rounded-xl p-4 text-center">
                  <div className="text-2xl font-black text-blue-400">{org.followers_count}</div>
                  <div className="text-white/50 text-xs">Followers</div>
                </div>
                <div className="bg-white/5 rounded-xl p-4 text-center">
                  <div className="text-2xl font-black text-white">{org.posts_count}</div>
                  <div className="text-white/50 text-xs">Total Posts</div>
                </div>
                <div className="bg-white/5 rounded-xl p-4 text-center">
                  <div className="text-2xl font-black text-green-400">{org.posts_7d}</div>
                  <div className="text-white/50 text-xs">Posts (7d)</div>
                </div>
              </div>

              {/* Engagement */}
              <div className="flex gap-6 mb-6 text-sm">
                <div className="flex items-center gap-2">
                  <span className="text-pink-400">&#x2764;</span>
                  <span className="text-white/60">{org.engagement?.total_likes || 0} total likes</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-blue-400">&#x1F4AC;</span>
                  <span className="text-white/60">{org.engagement?.total_comments || 0} total comments</span>
                </div>
              </div>

              {/* Recent Posts */}
              {org.recent_posts?.length > 0 && (
                <div>
                  <h3 className="text-sm font-bold text-white/60 uppercase mb-3">Recent Posts</h3>
                  <div className="space-y-2">
                    {org.recent_posts.map((post: any, i: number) => (
                      <div key={post.id || i} className="bg-white/5 rounded-lg p-3 flex justify-between items-center">
                        <div>
                          <div className="text-white/80 text-sm font-medium">{post.title || 'Untitled'}</div>
                          <div className="text-white/40 text-xs line-clamp-1">{post.content}</div>
                        </div>
                        <div className="flex gap-3 text-xs text-white/30">
                          <span>&#x2764; {post.likes_count}</span>
                          <span>&#x1F4AC; {post.comments_count}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}

          {(!data.organizations || data.organizations.length === 0) && (
            <Card>
              <p className="text-white/50 text-center py-8">You don't manage any organizations yet.</p>
            </Card>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default OrgLeaderDashboard;
