// Profile Page Component

import React from 'react';
import { Layout } from '@/components/layout';
import { Card, Avatar } from '@/components/ui';
import { useAuth } from '@/hooks';
import { Mail, Calendar } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

const ProfilePage: React.FC = () => {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <Layout>
      <div className="px-6 max-w-4xl mx-auto">
        <Card>
          {/* Header */}
          <div className="flex items-start gap-6 mb-8">
            <Avatar
              src={user.profile_picture}
              alt={user.first_name}
              size="xl"
              fallback={user.first_name?.[0]}
            />

            <div className="flex-1">
              <h1 className="text-3xl font-black mb-1">
                {user.first_name} {user.last_name}
              </h1>
              <p className="text-white/60 mb-4">@{user.username || user.email}</p>

              {user.bio && <p className="text-white/80 mb-4">{user.bio}</p>}

              <div className="flex items-center gap-6 text-sm text-white/60">
                <div className="flex items-center gap-2">
                  <Mail size={16} />
                  <span>{user.email}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar size={16} />
                  <span>
                    Joined {formatDistanceToNow(new Date(user.date_joined || user.created_at), { addSuffix: true })}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 pt-6 border-t border-white/10">
            <div className="text-center">
              <div className="text-2xl font-bold text-msu-gold mb-1">0</div>
              <div className="text-sm text-white/60">Organizations</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-msu-gold mb-1">0</div>
              <div className="text-sm text-white/60">Posts</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-msu-gold mb-1">0</div>
              <div className="text-sm text-white/60">Following</div>
            </div>
          </div>
        </Card>
      </div>
    </Layout>
  );
};

export default ProfilePage;
