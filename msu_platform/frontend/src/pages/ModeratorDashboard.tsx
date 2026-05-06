// Moderator Dashboard - Community Safety Panel
// Content monitoring, rule enforcement, moderation stats

import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Layout } from '@/components/layout';
import { Card, Spinner } from '@/components/ui';
import { apiClient } from '@/services/api';
import { API_ENDPOINTS, QUERY_KEYS } from '@/utils/constants';

const ModeratorDashboard: React.FC = () => {
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: [QUERY_KEYS.DASHBOARD_MODERATOR],
    queryFn: async () => {
      const res = await apiClient.get(API_ENDPOINTS.DASHBOARD_MODERATOR);
      return res.data;
    },
    refetchInterval: 15000,
  });

  const togglePost = useMutation({
    mutationFn: async (postId: string) => {
      return apiClient.post(API_ENDPOINTS.MOD_TOGGLE_POST(postId));
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.DASHBOARD_MODERATOR] }),
  });

  if (isLoading) {
    return <Layout><div className="flex justify-center py-32"><Spinner size="lg" /></div></Layout>;
  }

  if (error || !data) {
    return <Layout><div className="max-w-7xl mx-auto px-6"><Card><p className="text-red-400">Access denied.</p></Card></div></Layout>;
  }

  const { content_stats, user_stats, recent_posts, recent_security } = data;

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-6 animate-in">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">&#x1F6E1;</span>
            <h1 className="text-4xl font-black text-gradient">Moderation Panel</h1>
          </div>
          <p className="text-white/50">Monitor content, enforce rules, keep the community safe.</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="glass-dark rounded-2xl p-5">
            <div className="text-2xl font-black text-blue-400">{content_stats.posts_24h}</div>
            <div className="text-white/50 text-sm">Posts (24h)</div>
          </div>
          <div className="glass-dark rounded-2xl p-5">
            <div className="text-2xl font-black text-msu-gold">{content_stats.comments_24h}</div>
            <div className="text-white/50 text-sm">Comments (24h)</div>
          </div>
          <div className="glass-dark rounded-2xl p-5">
            <div className={`text-2xl font-black ${content_stats.flagged_posts > 0 ? 'text-red-400' : 'text-green-400'}`}>{content_stats.flagged_posts}</div>
            <div className="text-white/50 text-sm">Flagged Posts</div>
          </div>
          <div className="glass-dark rounded-2xl p-5">
            <div className={`text-2xl font-black ${user_stats.suspended_users > 0 ? 'text-orange-400' : 'text-green-400'}`}>{user_stats.suspended_users}</div>
            <div className="text-white/50 text-sm">Suspended Users</div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Recent Posts for Review */}
          <div className="lg:col-span-2">
            <h2 className="text-lg font-bold text-white/80 mb-4 uppercase tracking-wider">Recent Posts</h2>
            <div className="space-y-3">
              {recent_posts?.map((post: any, i: number) => (
                <div key={post.id || i} className="glass-dark rounded-xl p-4 hover:bg-white/5 transition-colors">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-white/80 font-semibold text-sm">{post.author__first_name} {post.author__last_name}</span>
                        <span className="text-white/30 text-xs">{post.author__email}</span>
                      </div>
                      {post.title && <div className="text-white font-bold text-sm mb-1">{post.title}</div>}
                      <p className="text-white/60 text-sm line-clamp-2">{post.content}</p>
                      <div className="flex gap-4 mt-2 text-xs text-white/30">
                        <span>&#x2764; {post.likes_count}</span>
                        <span>&#x1F4AC; {post.comments_count}</span>
                        <span>{new Date(post.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                    <button
                      onClick={() => togglePost.mutate(post.id)}
                      className={`ml-4 px-3 py-1.5 rounded-lg text-xs font-bold transition-all hover:scale-105 ${
                        post.is_active
                          ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30'
                          : 'bg-green-500/20 text-green-400 hover:bg-green-500/30'
                      }`}
                    >
                      {post.is_active ? 'Hide' : 'Restore'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Security Alerts */}
          <div>
            <h2 className="text-lg font-bold text-white/80 mb-4 uppercase tracking-wider">Security Alerts</h2>
            <div className="space-y-3">
              {recent_security?.map((evt: any, i: number) => (
                <div key={evt.id || i} className="glass-dark rounded-xl p-4">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`w-2 h-2 rounded-full ${
                      evt.severity === 'CRITICAL' ? 'bg-red-500 animate-pulse' :
                      evt.severity === 'HIGH' ? 'bg-orange-500' : 'bg-yellow-500'
                    }`} />
                    <span className="text-white/80 text-sm font-semibold">{evt.event_type.replace(/_/g, ' ')}</span>
                  </div>
                  <p className="text-white/50 text-xs">{evt.description}</p>
                  <div className="flex justify-between mt-2">
                    <span className="text-white/30 text-xs">{new Date(evt.timestamp).toLocaleString()}</span>
                    <span className={`text-xs font-bold ${evt.resolved ? 'text-green-400' : 'text-red-400'}`}>
                      {evt.resolved ? 'Resolved' : 'Open'}
                    </span>
                  </div>
                </div>
              ))}
              {(!recent_security || recent_security.length === 0) && (
                <div className="glass-dark rounded-xl p-6 text-center text-white/30 text-sm">No recent security alerts</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ModeratorDashboard;
