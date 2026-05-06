// Admin Dashboard - System Administrator "God Mode" Panel
// Full access to all system features and data. All actions logged.

import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Layout } from '@/components/layout';
import { Card, Spinner } from '@/components/ui';
import { apiClient } from '@/services/api';
import { API_ENDPOINTS, QUERY_KEYS } from '@/utils/constants';
import { useRoles } from '@/hooks/useRoles';

const StatCard: React.FC<{ label: string; value: number | string; icon: string; color?: string }> = ({
  label, value, icon, color = 'text-msu-gold'
}) => (
  <div className="glass-dark rounded-2xl p-5 flex items-center gap-4 hover:scale-[1.02] transition-transform">
    <div className={`text-3xl ${color}`}>{icon}</div>
    <div>
      <div className={`text-2xl font-black ${color}`}>{value}</div>
      <div className="text-white/50 text-sm">{label}</div>
    </div>
  </div>
);

const AdminDashboard: React.FC = () => {
  const { isAdmin } = useRoles();
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: [QUERY_KEYS.DASHBOARD_ADMIN],
    queryFn: async () => {
      const res = await apiClient.get(API_ENDPOINTS.DASHBOARD_ADMIN);
      return res.data;
    },
    enabled: isAdmin,
    refetchInterval: 30000,
  });

  const assignRoleMutation = useMutation({
    mutationFn: async (payload: { email: string; role: string; organization_type?: string; organization_id?: number }) => {
      return apiClient.post(API_ENDPOINTS.ADMIN_ASSIGN_ROLE, payload);
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.DASHBOARD_ADMIN] }),
  });

  if (isLoading) {
    return (
      <Layout>
        <div className="flex justify-center py-32"><Spinner size="lg" /></div>
      </Layout>
    );
  }

  if (error || !data) {
    return (
      <Layout>
        <div className="max-w-7xl mx-auto px-6">
          <Card><p className="text-red-400">Access denied or failed to load admin data.</p></Card>
        </div>
      </Layout>
    );
  }

  const { overview, organizations, content, security, recent_audit } = data;

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-6 animate-in">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">&#x1F6E1;</span>
            <h1 className="text-4xl font-black text-gradient">System Admin</h1>
          </div>
          <p className="text-white/50">Full platform control. All actions are logged and auditable.</p>
        </div>

        {/* Overview Stats */}
        <section className="mb-8">
          <h2 className="text-lg font-bold text-white/80 mb-4 uppercase tracking-wider">Platform Overview</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard icon="&#x1F465;" label="Total Users" value={overview.total_users} />
            <StatCard icon="&#x1F4C8;" label="Active (30d)" value={overview.active_users_30d} color="text-green-400" />
            <StatCard icon="&#x1F195;" label="New (7d)" value={overview.new_users_7d} color="text-blue-400" />
            <StatCard icon="&#x2705;" label="Verified" value={overview.verified_users} color="text-emerald-400" />
          </div>
        </section>

        {/* Organizations */}
        <section className="mb-8">
          <h2 className="text-lg font-bold text-white/80 mb-4 uppercase tracking-wider">Organizations</h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <StatCard icon="&#x1F3DB;" label="Clubs" value={organizations.clubs} />
            <StatCard icon="&#x26EA;" label="Churches" value={organizations.churches} />
            <StatCard icon="&#x26BD;" label="Sports Teams" value={organizations.sports_teams} />
            <StatCard icon="&#x1F4C5;" label="Activities" value={organizations.activities} />
            <StatCard icon="&#x23F3;" label="Pending Approval" value={organizations.pending_approval} color="text-orange-400" />
          </div>
        </section>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Content Stats */}
          <section>
            <h2 className="text-lg font-bold text-white/80 mb-4 uppercase tracking-wider">Content</h2>
            <div className="glass-dark rounded-2xl p-6 space-y-4">
              <div className="flex justify-between"><span className="text-white/60">Total Posts</span><span className="font-bold text-msu-gold">{content.total_posts}</span></div>
              <div className="flex justify-between"><span className="text-white/60">Posts (7d)</span><span className="font-bold text-blue-400">{content.posts_7d}</span></div>
              <div className="flex justify-between"><span className="text-white/60">Comments</span><span className="font-bold text-white">{content.total_comments}</span></div>
              <div className="flex justify-between"><span className="text-white/60">Likes</span><span className="font-bold text-pink-400">{content.total_likes}</span></div>
            </div>
          </section>

          {/* Security */}
          <section>
            <h2 className="text-lg font-bold text-white/80 mb-4 uppercase tracking-wider">Security</h2>
            <div className="glass-dark rounded-2xl p-6 space-y-4">
              <div className="flex justify-between"><span className="text-white/60">Events (7d)</span><span className="font-bold text-white">{security.events_7d}</span></div>
              <div className="flex justify-between"><span className="text-white/60">Unresolved</span><span className={`font-bold ${security.unresolved_events > 0 ? 'text-orange-400' : 'text-green-400'}`}>{security.unresolved_events}</span></div>
              <div className="flex justify-between"><span className="text-white/60">Critical</span><span className={`font-bold ${security.critical_events > 0 ? 'text-red-500 animate-pulse' : 'text-green-400'}`}>{security.critical_events}</span></div>
            </div>
          </section>
        </div>

          {/* Role Management */}
          <section className="mt-8">
            <h2 className="text-lg font-bold text-white/80 mb-4 uppercase tracking-wider">Role & Community Management</h2>
            <div className="glass-dark rounded-2xl p-6">
              <form 
                onSubmit={(e) => {
                  e.preventDefault();
                  const formData = new FormData(e.currentTarget);
                  const email = formData.get('email') as string;
                  const role = formData.get('role') as string;
                  const orgType = formData.get('org_type') as string;
                  const orgId = Number(formData.get('org_id'));

                  assignRoleMutation.mutate({
                    email, role, 
                    ...(orgType && orgId ? { organization_type: orgType, organization_id: orgId } : {})
                  });
                  e.currentTarget.reset();
                }}
                className="grid grid-cols-1 md:grid-cols-5 gap-4 items-end"
              >
                <div>
                  <label className="block text-xs text-white/50 mb-1">User Email</label>
                  <input name="email" type="email" required placeholder="user@msu.ac.zw" className="w-full bg-white/5 border border-white/10 rounded p-2 text-sm focus:border-msu-gold outline-none" />
                </div>
                <div>
                  <label className="block text-xs text-white/50 mb-1">Role Name</label>
                  <input name="role" type="text" required placeholder="e.g. Club President" className="w-full bg-white/5 border border-white/10 rounded p-2 text-sm focus:border-msu-gold outline-none" />
                </div>
                <div>
                  <label className="block text-xs text-white/50 mb-1">Org Type (Optional)</label>
                  <select name="org_type" className="w-full bg-white/5 border border-white/10 rounded p-2 text-sm focus:border-msu-gold outline-none text-white/70">
                    <option value="">System-wide</option>
                    <option value="club">Club</option>
                    <option value="church">Church</option>
                    <option value="sportsteam">Sports Team</option>
                    <option value="activity">Activity</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-white/50 mb-1">Org ID (Optional)</label>
                  <input name="org_id" type="number" placeholder="ID" className="w-full bg-white/5 border border-white/10 rounded p-2 text-sm focus:border-msu-gold outline-none" />
                </div>
                <div>
                  <button 
                    type="submit" 
                    disabled={assignRoleMutation.isPending}
                    className="w-full bg-msu-gold hover:bg-msu-gold-hover text-black font-bold py-2 px-4 rounded transition-colors disabled:opacity-50 text-sm"
                  >
                    {assignRoleMutation.isPending ? 'Assigning...' : 'Assign Role'}
                  </button>
                </div>
              </form>
              {assignRoleMutation.isError && (
                <p className="text-red-400 mt-2 text-sm text-center">Failed to assign role. Check details.</p>
              )}
              {assignRoleMutation.isSuccess && (
                <p className="text-green-400 mt-2 text-sm text-center">Role assigned successfully.</p>
              )}
            </div>
            
            <div className="glass-dark rounded-2xl p-6 mt-4">
              <h3 className="text-md font-bold text-white/80 mb-4">Create Organization (Quick Add)</h3>
              <form 
                onSubmit={async (e) => {
                  e.preventDefault();
                  const formData = new FormData(e.currentTarget);
                  const orgType = formData.get('org_type') as string;
                  const name = formData.get('name') as string;
                  const description = formData.get('description') as string;
                  
                  const endpointMap: Record<string, string> = {
                    club: API_ENDPOINTS.CLUBS,
                    church: API_ENDPOINTS.CHURCHES,
                    sportsteam: API_ENDPOINTS.SPORTS_TEAMS,
                    activity: API_ENDPOINTS.ACTIVITIES
                  };

                  try {
                    await apiClient.post(endpointMap[orgType], { name, description });
                    alert('Organization created successfully!');
                    queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.DASHBOARD_ADMIN] });
                    e.currentTarget.reset();
                  } catch (err) {
                    alert('Failed to create organization.');
                  }
                }}
                className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end"
              >
                <div>
                  <label className="block text-xs text-white/50 mb-1">Type</label>
                  <select name="org_type" required className="w-full bg-white/5 border border-white/10 rounded p-2 text-sm focus:border-msu-gold outline-none text-white/70">
                    <option value="club">Club</option>
                    <option value="church">Church</option>
                    <option value="sportsteam">Sports Team</option>
                    <option value="activity">Activity</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-white/50 mb-1">Name</label>
                  <input name="name" type="text" required placeholder="e.g. AI Society" className="w-full bg-white/5 border border-white/10 rounded p-2 text-sm focus:border-msu-gold outline-none" />
                </div>
                <div>
                  <label className="block text-xs text-white/50 mb-1">Description</label>
                  <input name="description" type="text" required placeholder="Short bio..." className="w-full bg-white/5 border border-white/10 rounded p-2 text-sm focus:border-msu-gold outline-none" />
                </div>
                <div>
                  <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded transition-colors text-sm">
                    Create Org
                  </button>
                </div>
              </form>
            </div>
          </section>

        {/* Audit Trail */}
        <section className="mt-8">
          <h2 className="text-lg font-bold text-white/80 mb-4 uppercase tracking-wider">Recent Audit Log</h2>
          <div className="glass-dark rounded-2xl overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/10 text-white/40 uppercase text-xs">
                  <th className="text-left p-4">Action</th>
                  <th className="text-left p-4">User</th>
                  <th className="text-left p-4">IP</th>
                  <th className="text-left p-4">Time</th>
                </tr>
              </thead>
              <tbody>
                {Array.isArray(recent_audit) && recent_audit.map((log: any, i: number) => (
                  <tr key={log.id || i} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="p-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                        log.action === 'CREATE' ? 'bg-green-500/20 text-green-400' :
                        log.action === 'DELETE' ? 'bg-red-500/20 text-red-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>{log.action}</span>
                    </td>
                    <td className="p-4 text-white/70">{log.user__email || 'System'}</td>
                    <td className="p-4 text-white/40 font-mono text-xs">{log.ip_address}</td>
                    <td className="p-4 text-white/40 text-xs">{new Date(log.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
                {(!recent_audit || recent_audit.length === 0) && (
                  <tr><td colSpan={4} className="p-8 text-center text-white/30">No audit logs yet</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default AdminDashboard;
