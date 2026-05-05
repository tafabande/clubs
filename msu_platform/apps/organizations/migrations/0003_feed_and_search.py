"""
Migration for feed and search functionality.

This migration creates models for:
- Social feed (Post, PostMedia, PostLike, PostComment, PostShare, Feed)
- Search functionality (SearchIndex, PopularSearch)
"""
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    """Feed and search models migration."""

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0001_initial'),
        ('organizations', '0002_enable_rls'),
    ]

    operations = [
        # ============================================================================
        # POST MODEL
        # ============================================================================
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('object_id', models.UUIDField(help_text='ID of the organization')),
                ('post_type', models.CharField(
                    choices=[
                        ('announcement', 'Announcement'),
                        ('event', 'Event'),
                        ('achievement', 'Achievement'),
                        ('general', 'General Update'),
                        ('media', 'Media Post'),
                        ('recruitment', 'Recruitment'),
                    ],
                    default='general',
                    max_length=20
                )),
                ('title', models.CharField(blank=True, help_text='Optional title for post', max_length=200)),
                ('content', models.TextField(help_text='Post content/description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='posts/videos/')),
                ('event_date', models.DateTimeField(blank=True, help_text='Event date and time', null=True)),
                ('event_location', models.CharField(blank=True, help_text='Event location', max_length=200)),
                ('event_link', models.URLField(blank=True, help_text='Event registration or info link')),
                ('visibility', models.CharField(
                    choices=[
                        ('public', 'Public'),
                        ('members_only', 'Members Only'),
                        ('admin_only', 'Admin Only'),
                    ],
                    default='public',
                    max_length=20
                )),
                ('is_pinned', models.BooleanField(default=False, help_text='Pin post to top of feed')),
                ('likes_count', models.IntegerField(default=0)),
                ('comments_count', models.IntegerField(default=0)),
                ('shares_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('tags', models.CharField(blank=True, help_text='Comma-separated tags', max_length=500)),
                ('author', models.ForeignKey(
                    help_text='User who created the post',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='posts',
                    to='users.user'
                )),
                ('content_type', models.ForeignKey(
                    help_text='Type of organization (Club, Church, Sports Team, Activity)',
                    on_delete=django.db.models.deletion.CASCADE,
                    to='contenttypes.contenttype'
                )),
            ],
            options={
                'db_table': 'posts',
                'ordering': ['-is_pinned', '-created_at'],
            },
        ),

        # ============================================================================
        # POST MEDIA MODEL
        # ============================================================================
        migrations.CreateModel(
            name='PostMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('media_type', models.CharField(
                    choices=[
                        ('image', 'Image'),
                        ('video', 'Video'),
                        ('document', 'Document'),
                    ],
                    max_length=20
                )),
                ('file', models.FileField(upload_to='posts/media/')),
                ('caption', models.CharField(blank=True, max_length=500)),
                ('order', models.IntegerField(default=0, help_text='Display order')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='media',
                    to='organizations.post'
                )),
            ],
            options={
                'db_table': 'post_media',
                'ordering': ['order', 'created_at'],
            },
        ),

        # ============================================================================
        # POST LIKE MODEL
        # ============================================================================
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='likes',
                    to='organizations.post'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='post_likes',
                    to='users.user'
                )),
            ],
            options={
                'db_table': 'post_likes',
                'unique_together': {('post', 'user')},
            },
        ),

        # ============================================================================
        # POST COMMENT MODEL
        # ============================================================================
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('likes_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(
                    blank=True,
                    help_text='Parent comment for nested replies',
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='replies',
                    to='organizations.postcomment'
                )),
                ('post', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comments',
                    to='organizations.post'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='post_comments',
                    to='users.user'
                )),
            ],
            options={
                'db_table': 'post_comments',
                'ordering': ['-created_at'],
            },
        ),

        # ============================================================================
        # POST SHARE MODEL
        # ============================================================================
        migrations.CreateModel(
            name='PostShare',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='shares',
                    to='organizations.post'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='post_shares',
                    to='users.user'
                )),
            ],
            options={
                'db_table': 'post_shares',
            },
        ),

        # ============================================================================
        # FEED MODEL
        # ============================================================================
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('relevance_score', models.FloatField(default=1.0)),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='organizations.post'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='feeds',
                    to='users.user'
                )),
            ],
            options={
                'db_table': 'feeds',
                'ordering': ['-relevance_score', '-created_at'],
                'unique_together': {('user', 'post')},
            },
        ),

        # ============================================================================
        # SEARCH INDEX MODEL
        # ============================================================================
        migrations.CreateModel(
            name='SearchIndex',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('organization_type', models.CharField(
                    choices=[
                        ('club', 'Club'),
                        ('church', 'Church'),
                        ('sports_team', 'Sports Team'),
                        ('activity', 'Activity'),
                    ],
                    max_length=50
                )),
                ('organization_id', models.UUIDField()),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.CharField(blank=True, max_length=100)),
                ('tags', models.TextField(blank=True, help_text='Space-separated tags')),
                ('is_active', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('member_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'search_index',
            },
        ),

        # ============================================================================
        # POPULAR SEARCH MODEL
        # ============================================================================
        migrations.CreateModel(
            name='PopularSearch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('query', models.CharField(max_length=200, unique=True)),
                ('search_count', models.IntegerField(default=1)),
                ('last_searched', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'popular_searches',
                'ordering': ['-search_count', '-last_searched'],
            },
        ),

        # ============================================================================
        # INDEXES
        # ============================================================================
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-created_at'], name='posts_created_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['content_type', 'object_id'], name='posts_org_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['post_type', '-created_at'], name='posts_type_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['is_pinned', '-created_at'], name='posts_pinned_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['visibility', '-created_at'], name='posts_vis_idx'),
        ),
        migrations.AddIndex(
            model_name='postlike',
            index=models.Index(fields=['post', 'user'], name='likes_post_user_idx'),
        ),
        migrations.AddIndex(
            model_name='postlike',
            index=models.Index(fields=['user', '-created_at'], name='likes_user_idx'),
        ),
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['post', '-created_at'], name='comments_post_idx'),
        ),
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['user', '-created_at'], name='comments_user_idx'),
        ),
        migrations.AddIndex(
            model_name='postshare',
            index=models.Index(fields=['post', '-created_at'], name='shares_post_idx'),
        ),
        migrations.AddIndex(
            model_name='postshare',
            index=models.Index(fields=['user', '-created_at'], name='shares_user_idx'),
        ),
        migrations.AddIndex(
            model_name='feed',
            index=models.Index(fields=['user', '-created_at'], name='feeds_user_idx'),
        ),
        migrations.AddIndex(
            model_name='feed',
            index=models.Index(fields=['user', '-relevance_score'], name='feeds_relevance_idx'),
        ),
        migrations.AddIndex(
            model_name='feed',
            index=models.Index(fields=['is_read', '-created_at'], name='feeds_read_idx'),
        ),
        migrations.AddIndex(
            model_name='searchindex',
            index=models.Index(fields=['organization_type', 'is_active'], name='search_type_idx'),
        ),
        migrations.AddIndex(
            model_name='searchindex',
            index=models.Index(fields=['is_approved', '-member_count'], name='search_approved_idx'),
        ),
        migrations.AddIndex(
            model_name='searchindex',
            index=models.Index(fields=['category', '-member_count'], name='search_category_idx'),
        ),
        migrations.AddIndex(
            model_name='popularsearch',
            index=models.Index(fields=['-search_count'], name='popular_count_idx'),
        ),
    ]
