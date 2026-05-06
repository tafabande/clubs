// Post Card Component

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Heart, MessageSquare, Share2, CheckCircle2 } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { Card, Avatar, Button } from '@/components/ui';
import { useAuth, useTogglePostLike } from '@/hooks';
import type { Post } from '@/types';

interface PostCardProps {
  post: Post;
}

export const PostCard: React.FC<PostCardProps> = ({ post }) => {
  const toggleLike = useTogglePostLike();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLike = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    try {
      await toggleLike.mutateAsync({
        id: post.id,
        isLiked: post.is_liked || false,
      });
    } catch (error) {
      console.error('Failed to toggle like:', error);
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: `Post from ${post.organization.name}`,
        text: post.content,
        url: window.location.href,
      }).catch(console.error);
    }
  };

  return (
    <Card hover className="mb-6">
      {/* Header */}
      <div className="flex items-start gap-4 mb-4">
        <div className="relative">
          <Avatar
            src={post.author.profile_picture}
            alt={post.author.first_name}
            fallback={post.author.first_name?.[0]}
            className="border-2 border-white dark:border-slate-800 shadow-sm"
          />
          {post.organization?.logo && (
            <div className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full border-2 border-white dark:border-slate-900 overflow-hidden bg-white shadow-sm">
              <img 
                src={post.organization.logo} 
                alt={post.organization.name} 
                className="w-full h-full object-cover"
              />
            </div>
          )}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <h4 className="font-bold text-slate-900 dark:text-white flex items-center gap-1">
                {post.author.first_name} {post.author.last_name}
                {post.author.is_verified && (
                  <CheckCircle2 size={14} className="text-blue-400 fill-blue-400/20" />
                )}
              </h4>
              <span className="text-slate-500 dark:text-white/40 text-sm hidden sm:inline">@{post.author.username || post.author.email.split('@')[0]}</span>
            </div>
            <span className="text-slate-400 dark:text-white/30 text-xs">
              {(() => {
                const date = new Date(post.created_at);
                return !isNaN(date.getTime()) 
                  ? formatDistanceToNow(date, { addSuffix: true }) 
                  : 'Just now';
              })()}
            </span>
          </div>
          <div className="flex items-center gap-2 mt-0.5">
            <Link 
              to={`/organizations/${post.organization?.organization_type || 'club'}/${post.organization?.id}`} 
              className="text-msu-blue dark:text-msu-gold hover:underline text-sm font-semibold truncate"
            >
              {post.organization?.name || 'Unknown Organization'}
            </Link>
          </div>
        </div>
      </div>

      {/* Content */}
      {post.title && <h3 className="text-xl font-bold mb-2 text-slate-900 dark:text-white">{post.title}</h3>}
      <p className="text-slate-800 dark:text-white/80 mb-4 whitespace-pre-wrap leading-relaxed">{post.content}</p>

      {/* Media */}
      {post.image && (
        <div className="mb-4 rounded-xl overflow-hidden bg-slate-100 dark:bg-white/5">
          <img
            src={post.image}
            alt="Post content"
            className="w-full max-h-[500px] object-cover hover:scale-[1.02] transition-transform duration-500"
          />
        </div>
      )}

      {Array.isArray(post.media) && post.media.length > 0 && (
        <div className={`grid ${post.media.length === 1 ? 'grid-cols-1' : 'grid-cols-2'} gap-2 mb-4 rounded-xl overflow-hidden`}>
          {post.media.slice(0, 4).map((media) => (
            <div key={media.id} className="aspect-video bg-slate-100 dark:bg-white/5 relative group">
              {media.media_type === 'image' && (
                <img
                  src={media.file_url}
                  alt={media.caption || 'Post media'}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
                />
              )}
              {media.media_type === 'video' && (
                <video
                  src={media.file_url}
                  poster={media.thumbnail_url}
                  className="w-full h-full object-cover"
                />
              )}
              {media.caption && (
                <div className="absolute bottom-0 left-0 right-0 p-2 bg-black/50 text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity">
                  {media.caption}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-6 pt-4 border-t border-slate-200 dark:border-white/10">
        <Button
          variant="ghost"
          size="sm"
          onClick={handleLike}
          className={`hover:bg-red-500/10 ${post.is_liked ? 'text-red-500 hover:text-red-600' : 'text-slate-500 dark:text-white/50 hover:text-red-500'}`}
        >
          <Heart size={18} fill={post.is_liked ? 'currentColor' : 'none'} className="transition-transform active:scale-75" />
          <span className="font-medium">{post.likes_count}</span>
        </Button>

        <Button 
          variant="ghost" 
          size="sm"
          onClick={() => {
            if (!isAuthenticated) navigate('/login');
          }}
          className="text-slate-500 dark:text-white/50 hover:text-msu-blue dark:hover:text-msu-gold hover:bg-msu-blue/10 dark:hover:bg-msu-gold/10"
        >
          <MessageSquare size={18} />
          <span className="font-medium">{post.comments_count}</span>
        </Button>

        <Button 
          variant="ghost" 
          size="sm"
          onClick={handleShare}
          className="text-slate-500 dark:text-white/50 hover:text-msu-blue dark:hover:text-msu-gold hover:bg-msu-blue/10 dark:hover:bg-msu-gold/10 ml-auto"
        >
          <Share2 size={18} />
        </Button>
      </div>
    </Card>
  );
};

export default PostCard;
