import React, { useState } from 'react';
import { Layout } from '@/components/layout';
import { Card, Button, Input, Spinner } from '@/components/ui';
import { useAuth } from '@/hooks';
import { User, Camera, Save, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { logger } from '@/utils/logger';

const SettingsPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, updateProfile, isUpdatingProfile } = useAuth();
  
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    bio: user?.bio || '',
    interests: user?.interests || '',
    faculty: user?.faculty || '',
    department: user?.department || '',
    phone: user?.phone || '',
  });

  const [profilePicture, setProfilePicture] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(user?.profile_picture || null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setProfilePicture(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    logger.info('Updating profile...', formData);
    
    try {
      await updateProfile({
        ...formData,
        profile_picture: profilePicture || undefined,
      });
      logger.info('Profile updated successfully');
      navigate('/profile');
    } catch (error) {
      logger.error('Failed to update profile:', error);
    }
  };

  if (!user) return null;

  return (
    <Layout>
      <div className="px-6 max-w-4xl mx-auto animate-in">
        <div className="flex items-center gap-4 mb-8">
          <button 
            onClick={() => navigate(-1)}
            className="p-2 hover:bg-white/10 rounded-xl transition-colors"
          >
            <ArrowLeft size={24} />
          </button>
          <h1 className="text-3xl font-black">Personalise Profile</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          <Card className="overflow-visible">
            <div className="flex flex-col md:flex-row gap-8 items-start">
              {/* Profile Picture Upload */}
              <div className="relative group mx-auto md:mx-0">
                <div className="w-32 h-32 rounded-3xl overflow-hidden ring-4 ring-msu-gold/20 relative">
                  {previewUrl ? (
                    <img src={previewUrl} alt="Preview" className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full bg-white/10 flex items-center justify-center">
                      <User size={48} className="text-white/20" />
                    </div>
                  )}
                  
                  <label className="absolute inset-0 bg-black/60 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                    <Camera size={24} className="text-white mb-1" />
                    <span className="text-[10px] font-bold text-white uppercase tracking-wider">Change</span>
                    <input 
                      type="file" 
                      className="hidden" 
                      accept="image/*" 
                      onChange={handleFileChange} 
                    />
                  </label>
                </div>
              </div>

              <div className="flex-1 grid md:grid-cols-2 gap-6 w-full">
                <div className="space-y-2">
                  <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">First Name</label>
                  <Input
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleInputChange}
                    placeholder="Enter first name"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">Last Name</label>
                  <Input
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleInputChange}
                    placeholder="Enter last name"
                    required
                  />
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <h3 className="text-lg font-bold mb-6 flex items-center gap-2 text-msu-gold">
              <User size={20} />
              About You
            </h3>
            <div className="space-y-6">
              <div className="space-y-2">
                <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">Bio</label>
                <textarea
                  name="bio"
                  value={formData.bio}
                  onChange={handleInputChange}
                  placeholder="Tell us about yourself..."
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder:text-white/20 focus:outline-none focus:ring-2 focus:ring-msu-gold/50 min-h-[120px] transition-all"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">Interests</label>
                <Input
                  name="interests"
                  value={formData.interests}
                  onChange={handleInputChange}
                  placeholder="e.g. Technology, Music, Sports"
                />
              </div>
            </div>
          </Card>

          <Card>
            <h3 className="text-lg font-bold mb-6 flex items-center gap-2 text-msu-gold">
              <Camera size={20} />
              Academic Info
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">Faculty</label>
                <Input
                  name="faculty"
                  value={formData.faculty}
                  onChange={handleInputChange}
                  placeholder="e.g. Science & Technology"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">Department</label>
                <Input
                  name="department"
                  value={formData.department}
                  onChange={handleInputChange}
                  placeholder="e.g. Computer Science"
                />
              </div>
            </div>
          </Card>

          <div className="flex justify-end gap-4">
            <Button 
              type="button" 
              variant="ghost" 
              onClick={() => navigate(-1)}
              disabled={isUpdatingProfile}
            >
              Cancel
            </Button>
            <Button 
              type="submit" 
              variant="gold" 
              className="px-8 shadow-lg shadow-msu-gold/20"
              disabled={isUpdatingProfile}
            >
              {isUpdatingProfile ? <Spinner size="sm" /> : <Save size={20} />}
              Save Changes
            </Button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default SettingsPage;
