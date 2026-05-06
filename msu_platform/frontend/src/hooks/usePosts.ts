// Posts Hook

import { useQuery, useMutation, useQueryClient, useInfiniteQuery } from '@tanstack/react-query';
import { postsService } from '@/services';
import { QUERY_KEYS, DEFAULT_PAGE_SIZE } from '@/utils/constants';
import type {
  PostFilters,
  CreatePostRequest,
  UpdatePostRequest,
  CreateCommentRequest,
} from '@/types';

/**
 * Get paginated posts (feed)
 */
export const usePosts = (filters?: PostFilters) => {
  return useQuery({
    queryKey: [QUERY_KEYS.POSTS, filters],
    queryFn: () => postsService.getPosts(filters),
  });
};

/**
 * Get infinite scroll posts
 */
export const useInfinitePosts = (filters?: PostFilters) => {
  return useInfiniteQuery({
    queryKey: [QUERY_KEYS.POSTS, 'infinite', filters],
    queryFn: ({ pageParam = 1 }) =>
      postsService.getPosts({
        ...filters,
        page: pageParam,
        page_size: DEFAULT_PAGE_SIZE,
      }),
    getNextPageParam: (lastPage, allPages) => {
      return lastPage.next ? allPages.length + 1 : undefined;
    },
    initialPageParam: 1,
  });
};

/**
 * Get single post by ID
 */
export const usePost = (id: number) => {
  return useQuery({
    queryKey: [QUERY_KEYS.POST, id],
    queryFn: () => postsService.getPost(id),
    enabled: !!id,
  });
};

/**
 * Get post comments
 */
export const usePostComments = (id: number) => {
  return useQuery({
    queryKey: [QUERY_KEYS.POST, id, 'comments'],
    queryFn: () => postsService.getPostComments(id),
    enabled: !!id,
  });
};

/**
 * Create post mutation
 */
export const useCreatePost = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreatePostRequest) => postsService.createPost(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.POSTS] });
    },
  });
};

/**
 * Update post mutation
 */
export const useUpdatePost = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdatePostRequest }) =>
      postsService.updatePost(id, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.POSTS] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.POST, variables.id] });
    },
  });
};

/**
 * Delete post mutation
 */
export const useDeletePost = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => postsService.deletePost(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.POSTS] });
    },
  });
};

/**
 * Like/Unlike post mutation
 */
export const useTogglePostLike = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, isLiked }: { id: number; isLiked: boolean }) =>
      postsService.toggleLike(id, isLiked),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.POST, variables.id] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.POSTS] });
    },
  });
};

/**
 * Create comment mutation
 */
export const useCreateComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ postId, data }: { postId: number; data: CreateCommentRequest }) =>
      postsService.createComment(postId, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({
        queryKey: [QUERY_KEYS.POST, variables.postId, 'comments']
      });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.POST, variables.postId] });
    },
  });
};
