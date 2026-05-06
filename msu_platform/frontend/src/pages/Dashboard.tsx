// Dashboard Page Component

import React from 'react';
import { Layout } from '@/components/layout';
import { Card, Spinner } from '@/components/ui';
import { PostCard } from '@/components/features';
import { useInfinitePosts } from '@/hooks';
import { useAuth } from '@/hooks';

const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const { data, isLoading, error, hasNextPage, fetchNextPage, isFetchingNextPage } =
    useInfinitePosts({ ordering: '-created_at' });

  const posts = data?.pages.flatMap((page) => page.results) || [];

  return (
    <Layout>
      <div className="px-6 max-w-7xl mx-auto">
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
            <Card>
              <h3 className="font-bold mb-4">Your Stats</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-white/60">Organizations</span>
                  <span className="font-bold text-msu-gold">0</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white/60">Posts</span>
                  <span className="font-bold text-msu-gold">{posts.length}</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default DashboardPage;
