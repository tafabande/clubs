// Post Card Component

import React from 'react';
import { Heart, MessageSquare, Share2 } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { Card, Avatar, Button } from '@/components/ui';
import { useTogglePostLike } from '@/hooks';
import type { Post } from '@/types';

interface PostCardProps {
  post: Post;
}

export const PostCard: React.FC<PostCardProps> = ({ post }) => {
  const toggleLike = useTogglePostLike();

  const handleLike = async () => {
    try {
      await toggleLike.mutateAsync({
        id: post.id,
        isLiked: post.is_liked || false,
      });
    } catch (error) {
      console.error('Failed to toggle like:', error);
    }
  };

  return (
    <Card>
      {/* Header */}
      <div className="flex items-start gap-4 mb-4">
        <Avatar
          src={post.author.profile_picture}
          alt={post.author.username}
          fallback={post.author.username?.[0]}
        />

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h4 className="font-bold">
              {post.author.first_name} {post.author.last_name}
            </h4>
            <span className="text-white/40 text-sm">@{post.author.username}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-white/40">
            <span>{post.organization.name}</span>
            <span>•</span>
            <span>{formatDistanceToNow(new Date(post.created_at), { addSuffix: true })}</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <p className="text-white/80 mb-4 whitespace-pre-wrap">{post.content}</p>

      {/* Media */}
      {post.media && post.media.length > 0 && (
        <div className="grid grid-cols-2 gap-2 mb-4 rounded-xl overflow-hidden">
          {post.media.slice(0, 4).map((media) => (
            <div key={media.id} className="aspect-square bg-white/5">
              {media.media_type === 'image' && (
                <img
                  src={media.file_url}
                  alt={media.caption || 'Post media'}
                  className="w-full h-full object-cover"
                />
              )}
              {media.media_type === 'video' && (
                <video
                  src={media.file_url}
                  poster={media.thumbnail_url}
                  controls
                  className="w-full h-full object-cover"
                />
              )}
            </div>
          ))}
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-6 pt-4 border-t border-white/10">
        <Button
          variant="ghost"
          size="sm"
          onClick={handleLike}
          className={post.is_liked ? 'text-red-500' : ''}
        >
          <Heart size={18} fill={post.is_liked ? 'currentColor' : 'none'} />
          <span>{post.likes_count}</span>
        </Button>

        <Button variant="ghost" size="sm">
          <MessageSquare size={18} />
          <span>{post.comments_count}</span>
        </Button>

        <Button variant="ghost" size="sm">
          <Share2 size={18} />
        </Button>
      </div>
    </Card>
  );
};

export default PostCard;
