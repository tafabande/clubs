// Organization Detail Page Component

import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Users, Calendar, Mail, Phone } from 'lucide-react';
import { Layout } from '@/components/layout';
import { Card, Spinner, Button, Badge } from '@/components/ui';
import { PostCard } from '@/components/features';
import { useAuth, useOrganization, useOrganizationPosts, useJoinOrganization, useLeaveOrganization } from '@/hooks';

const OrganizationDetailPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const { type, id } = useParams<{ type: string; id: string }>();
  const organizationId = id || '';
  const organizationType = type || 'club';

  // Ensure type is valid for API calls (handle 'sports-teams' vs 'sports_team')
  const apiType = organizationType.replace('-', '_');

  const { data: organization, isLoading, error } = useOrganization(organizationType, organizationId);
  const { data: postsData, isLoading: postsLoading } = useOrganizationPosts(organizationType, organizationId);
  const joinMutation = useJoinOrganization();
  const leaveMutation = useLeaveOrganization();

  const handleJoinLeave = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    try {
      if (organization?.is_member) {
        await leaveMutation.mutateAsync({ type: organizationType, id: organizationId });
      } else {
        await joinMutation.mutateAsync({ type: organizationType, id: organizationId });
      }
    } catch (error) {
      console.error('Failed to join/leave organization:', error);
    }
  };



  if (isLoading) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      </Layout>
    );
  }

  if (error || !organization) {
    return (
      <Layout>
        <div className="px-6 max-w-7xl mx-auto">
          <Card>
            <p className="text-red-400">Failed to load organization. Please try again.</p>
          </Card>
        </div>
      </Layout>
    );
  }

  const posts = Array.isArray(postsData?.results) ? postsData!.results : [];

  return (
    <Layout>
      <div className="px-6 max-w-7xl mx-auto">
        {/* Cover Photo */}
        {organization.cover_photo && (
          <div className="h-64 -mx-6 -mt-24 mb-8 overflow-hidden rounded-2xl">
            <img
              src={organization.cover_photo}
              alt={organization.name}
              className="w-full h-full object-cover"
            />
          </div>
        )}

        {/* Header */}
        <div className="flex items-start gap-6 mb-8">
          {organization.logo ? (
            <img
              src={organization.logo}
              alt={organization.name}
              className="w-24 h-24 rounded-2xl object-cover border-4 border-white/20"
            />
          ) : (
            <div className="w-24 h-24 rounded-2xl bg-white/10 flex items-center justify-center border-4 border-white/20">
              <span className="text-4xl font-bold text-msu-gold">
                {organization.name.charAt(0)}
              </span>
            </div>
          )}

          <div className="flex-1">
            <h1 className="text-4xl font-black mb-2">{organization.name}</h1>
            <div className="flex items-center gap-4 mb-4">
              <Badge>{organization.organization_type}</Badge>
              {isAuthenticated && organization.is_member && <Badge variant="success">Member</Badge>}
            </div>
            <p className="text-white/60 mb-4">{organization.description}</p>
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
          </div>

          <Button
            onClick={handleJoinLeave}
            variant={organization.is_member ? 'outline' : 'primary'}
            isLoading={joinMutation.isPending || leaveMutation.isPending}
          >
            {organization.is_member ? 'Leave' : 'Join'}
          </Button>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Posts */}
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-2xl font-bold">Recent Posts</h2>

            {postsLoading && (
              <div className="flex justify-center py-10">
                <Spinner />
              </div>
            )}

            {posts.length === 0 && !postsLoading && (
              <Card>
                <p className="text-white/60 text-center py-10">No posts yet</p>
              </Card>
            )}

            {Array.isArray(posts) && posts.map((post) => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card>
              <h3 className="font-bold mb-4">Contact</h3>
              <div className="space-y-3">
                {organization.contact_email && (
                  <div className="flex items-center gap-2 text-sm">
                    <Mail size={16} className="text-msu-gold" />
                    <a href={`mailto:${organization.contact_email}`} className="hover:text-msu-gold">
                      {organization.contact_email}
                    </a>
                  </div>
                )}
                {organization.contact_phone && (
                  <div className="flex items-center gap-2 text-sm">
                    <Phone size={16} className="text-msu-gold" />
                    <a href={`tel:${organization.contact_phone}`} className="hover:text-msu-gold">
                      {organization.contact_phone}
                    </a>
                  </div>
                )}
              </div>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default OrganizationDetailPage;
