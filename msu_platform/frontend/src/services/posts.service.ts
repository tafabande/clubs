// Posts Service

import api from './api';
import { API_ENDPOINTS } from '@/utils/constants';
import type {
  Post,
  PostDetail,
  PaginatedResponse,
  PostFilters,
  CreatePostRequest,
  UpdatePostRequest,
  PostComment,
  CreateCommentRequest,
} from '@/types';

export const postsService = {
  /**
   * Get all posts (feed)
   */
  async getPosts(filters?: PostFilters): Promise<PaginatedResponse<Post>> {
    const response = await api.get<PaginatedResponse<Post>>(
      API_ENDPOINTS.POSTS,
      { params: filters }
    );
    return response.data;
  },

  /**
   * Get post by ID
   */
  async getPost(id: number): Promise<PostDetail> {
    const response = await api.get<PostDetail>(API_ENDPOINTS.POST_DETAIL(id));
    return response.data;
  },

  /**
   * Create new post
   */
  async createPost(data: CreatePostRequest): Promise<Post> {
    const formData = new FormData();

    formData.append('organization_type', data.organization_type);
    formData.append('organization_id', String(data.organization_id));
    formData.append('content', data.content);

    // Add media files
    if (data.media_files) {
      data.media_files.forEach((file, index) => {
        formData.append(`media_${index}`, file);
      });
    }

    const response = await api.post<Post>(
      API_ENDPOINTS.POSTS,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  /**
   * Update post
   */
  async updatePost(id: number, data: UpdatePostRequest): Promise<Post> {
    const response = await api.patch<Post>(
      API_ENDPOINTS.POST_DETAIL(id),
      data
    );
    return response.data;
  },

  /**
   * Delete post
   */
  async deletePost(id: number): Promise<void> {
    await api.delete(API_ENDPOINTS.POST_DETAIL(id));
  },

  /**
   * Like post
   */
  async likePost(id: number): Promise<void> {
    await api.post(API_ENDPOINTS.POST_LIKE(id));
  },

  /**
   * Unlike post
   */
  async unlikePost(id: number): Promise<void> {
    await api.post(API_ENDPOINTS.POST_UNLIKE(id));
  },

  /**
   * Get post comments
   */
  async getPostComments(id: number): Promise<PaginatedResponse<PostComment>> {
    const response = await api.get<PaginatedResponse<PostComment>>(
      API_ENDPOINTS.POST_COMMENTS(id)
    );
    return response.data;
  },

  /**
   * Create comment on post
   */
  async createComment(postId: number, data: CreateCommentRequest): Promise<PostComment> {
    const response = await api.post<PostComment>(
      API_ENDPOINTS.POST_COMMENTS(postId),
      data
    );
    return response.data;
  },

  /**
   * Toggle like on post
   */
  async toggleLike(id: number, isLiked: boolean): Promise<void> {
    if (isLiked) {
      await this.unlikePost(id);
    } else {
      await this.likePost(id);
    }
  },
};

export default postsService;
