import React, { useState } from 'react';
import { Image as ImageIcon, Video, Send } from 'lucide-react';
import { Card, Avatar, Button } from '@/components/ui';
import { useAuth, useRoles, useCreatePost } from '@/hooks';

export const CreatePostWidget: React.FC = () => {
  const { user } = useAuth();
  const { ledOrganizations, isAdmin } = useRoles();
  const createPost = useCreatePost();
  
  const [content, setContent] = useState('');
  const [selectedOrg, setSelectedOrg] = useState<string>('');

  // If user doesn't lead any orgs, they can still post if they are admin,
  // but they need to select an org to post to. 
  // Wait, the backend requires an organization_id. 
  // For now, let's only allow posting if they have ledOrganizations.
  if (ledOrganizations.length === 0 && !isAdmin) {
    return null; // Regular users cannot create official organization posts, they can only comment/like
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim() || !selectedOrg) return;

    const [type, id] = selectedOrg.split(':');

    try {
      await createPost.mutateAsync({
        organization_type: type,
        organization_id: parseInt(id),
        content,
      });
      setContent('');
      setSelectedOrg('');
    } catch (error) {
      console.error('Failed to create post:', error);
    }
  };

  return (
    <Card className="mb-6 border border-msu-gold/20">
      <form onSubmit={handleSubmit}>
        <div className="flex gap-4">
          <Avatar
            src={user?.profile_picture}
            alt={user?.first_name}
            fallback={user?.first_name?.[0]}
          />
          <div className="flex-1">
            <select 
              value={selectedOrg}
              onChange={(e) => setSelectedOrg(e.target.value)}
              className="bg-white/5 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white/80 mb-3 w-full focus:outline-none focus:border-msu-gold"
              required
            >
              <option value="" disabled>Select organization to post as...</option>
              {ledOrganizations.map((org) => (
                <option key={`${org.type}:${org.id}`} value={`${org.type}:${org.id}`}>
                  {org.role} - {org.type}
                </option>
              ))}
            </select>
            
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Share an update with the community..."
              className="w-full bg-transparent resize-none outline-none text-white/90 placeholder:text-white/30"
              rows={3}
            />
          </div>
        </div>

        <div className="flex items-center justify-between mt-4 pt-4 border-t border-white/10">
          <div className="flex gap-2 text-white/40">
            <button type="button" className="p-2 rounded-full hover:bg-white/5 hover:text-msu-gold transition-colors">
              <ImageIcon size={20} />
            </button>
            <button type="button" className="p-2 rounded-full hover:bg-white/5 hover:text-msu-gold transition-colors">
              <Video size={20} />
            </button>
          </div>
          
          <Button 
            type="submit" 
            disabled={!content.trim() || !selectedOrg || createPost.isPending}
            className="btn-primary flex items-center gap-2"
          >
            {createPost.isPending ? 'Posting...' : (
              <>
                <Send size={16} />
                Post Update
              </>
            )}
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default CreatePostWidget;
