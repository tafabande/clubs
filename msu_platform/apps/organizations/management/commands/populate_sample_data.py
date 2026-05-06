"""
Management command to populate sample data for MSU Platform.

Specifically designed for Midlands State University (MSU) Gweru Campus, Zimbabwe.

Creates realistic sample data for:
- Users (MSU Gweru students)
- Clubs (Technology, Academic, Cultural, Professional, Volunteer)
- Churches (Religious organizations on campus)
- Sports Teams (MSU Gweru sports teams)
- Activities (Campus events and activities)
- Memberships
- Posts
- Engagement (likes, comments, shares)

Based on MSU Gweru's structure:
- 9 Faculties (Agriculture, Arts, Commerce, Education, Engineering, Law, Science & Technology, Social Sciences, Medicine)
- Main campus in Gweru with multiple halls of residence
- Student email format: @msu.ac.zw
- Campus culture and Zimbabwean context
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db import transaction
import random
from datetime import timedelta

from apps.organizations.models import (
    Club, ClubMembership,
    Church, ChurchMembership,
    SportsTeam, SportsTeamMembership,
    Activity, ActivityRegistration,
    Post, PostLike, PostComment, PostShare,
    SearchIndex
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with realistic sample data for MSU Platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing sample data before populating',
        )
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of sample users to create (default: 50)',
        )

    def handle(self, *args, **options):
        """Populate sample data."""
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        num_users = options['users']

        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('Midlands State University Gweru Campus'))
        self.stdout.write(self.style.SUCCESS('Sample Data Population'))
        self.stdout.write(self.style.SUCCESS('=' * 70 + '\n'))

        # Create sample data
        with transaction.atomic():
            users = self.create_users(num_users)
            clubs = self.create_clubs(users)
            churches = self.create_churches(users)
            teams = self.create_sports_teams(users)
            activities = self.create_activities(users)

            self.create_memberships(users, clubs, churches, teams)
            self.create_activity_registrations(users, activities)

            posts = self.create_posts(users, clubs, churches, teams, activities)
            self.create_engagement(users, posts)

            # Populate search index
            self.populate_search_index(clubs, churches, teams, activities)

        self.display_summary()

    def clear_data(self):
        """Clear existing sample data."""
        Post.objects.all().delete()
        Activity.objects.all().delete()
        SportsTeam.objects.all().delete()
        Church.objects.all().delete()
        Club.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        SearchIndex.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✅ Existing data cleared\n'))

    def create_users(self, count):
        """Create sample users."""
        self.stdout.write('Creating users...')

        first_names = [
            'Tanaka', 'Rumbi', 'Tinashe', 'Chipo', 'Tendai', 'Rudo',
            'Tariro', 'Nyasha', 'Blessing', 'Takudzwa', 'Tafadzwa', 'Rutendo',
            'Farai', 'Anesu', 'Simba', 'Tawanda', 'Vimbai', 'Kudzai',
            'Munashe', 'Panashe', 'Munyaradzi', 'Tichaona', 'Varaidzo', 'Kundai'
        ]

        last_names = [
            'Moyo', 'Ncube', 'Sibanda', 'Dube', 'Ndlovu', 'Mpofu',
            'Khumalo', 'Nkomo', 'Nyathi', 'Mthembu', 'Mlilo', 'Tshuma',
            'Banda', 'Phiri', 'Mwale', 'Tembo', 'Zimba', 'Mbewe'
        ]

        # MSU Gweru has 9 faculties
        faculties = [
            'Agriculture', 'Arts', 'Commerce', 'Education', 'Engineering',
            'Law', 'Science and Technology', 'Social Sciences', 'Medicine'
        ]
        departments = [
            'Computer Science', 'Business Management', 'Accounting', 'Psychology',
            'Economics', 'English', 'Mathematics', 'Physics', 'Chemistry',
            'Civil Engineering', 'Mechanical Engineering', 'Information Technology',
            'Banking and Finance', 'Marketing', 'Human Resources'
        ]

        users = []
        for i in range(count):
            first = random.choice(first_names)
            last = random.choice(last_names)
            email = f'{first.lower()}.{last.lower()}{i}@msu.ac.zw'

            user = User.objects.create_user(
                email=email,
                password='password123',  # In production, use secure passwords
                first_name=first,
                last_name=last,
                faculty=random.choice(faculties),
                department=random.choice(departments),
                year_of_study=random.randint(1, 4),
                student_id=f'MSU{2020 + random.randint(0, 4)}{random.randint(1000, 9999)}',
                is_active=True,
                is_verified=True
            )
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(users)} users'))
        return users

    def create_clubs(self, users):
        """Create sample clubs."""
        self.stdout.write('Creating clubs...')

        clubs_data = [
            # Technology Clubs
            {'name': 'MSU Tech Society', 'category': 'technology', 'description': 'For students passionate about technology, coding, and innovation. Weekly workshops and hackathons.'},
            {'name': 'Computer Science Club', 'category': 'technology', 'description': 'Advancing knowledge in computer science through projects, competitions, and guest lectures.'},
            {'name': 'Web Developers Association', 'category': 'technology', 'description': 'Learn web development, build projects, and network with industry professionals.'},
            {'name': 'Data Science Society', 'category': 'technology', 'description': 'Exploring data analytics, machine learning, and AI applications.'},

            # Academic Clubs
            {'name': 'Debate Society', 'category': 'academic', 'description': 'Sharpening critical thinking and public speaking skills through competitive debates.'},
            {'name': 'Law Students Association', 'category': 'academic', 'description': 'Supporting law students with moot courts, legal aid clinics, and career guidance.'},
            {'name': 'Business Club', 'category': 'professional', 'description': 'Entrepreneurship workshops, business competitions, and networking events.'},
            {'name': 'Economics Society', 'category': 'academic', 'description': 'Discussing economic theory and practice with guest speakers and case studies.'},
            {'name': 'Science Club', 'category': 'academic', 'description': 'Hands-on experiments, science fairs, and research presentations.'},

            # Cultural Clubs
            {'name': 'Drama Society', 'category': 'arts', 'description': 'Producing plays, musicals, and theatrical performances throughout the year.'},
            {'name': 'Music Club', 'category': 'arts', 'description': 'For musicians of all levels - from beginners to professionals. Regular jam sessions and concerts.'},
            {'name': 'Poetry Society', 'category': 'arts', 'description': 'Open mic nights, poetry slams, and creative writing workshops.'},
            {'name': 'Photography Club', 'category': 'arts', 'description': 'Learn photography techniques, photo walks, and exhibitions.'},
            {'name': 'Cultural Heritage Society', 'category': 'cultural', 'description': 'Celebrating Zimbabwean culture through traditional dance, music, and food.'},

            # Social & Volunteer
            {'name': 'Environmental Club', 'category': 'volunteer', 'description': 'Campus clean-ups, tree planting, and environmental awareness campaigns.'},
            {'name': 'Red Cross Society', 'category': 'volunteer', 'description': 'First aid training, blood donation drives, and disaster response.'},
            {'name': 'Rotaract Club', 'category': 'social', 'description': 'Community service projects, leadership development, and international exchanges.'},
            {'name': 'AIESEC MSU', 'category': 'professional', 'description': 'Global internships, cultural exchanges, and leadership conferences.'},

            # Professional Clubs
            {'name': 'Marketing Society', 'category': 'professional', 'description': 'Case competitions, industry visits, and career workshops.'},
            {'name': 'Accountants Club', 'category': 'professional', 'description': 'Supporting accounting students with exam preparation and career guidance.'},
            {'name': 'Engineering Society', 'category': 'professional', 'description': 'Technical workshops, design competitions, and industry partnerships.'},
        ]

        clubs = []
        for data in clubs_data:
            creator = random.choice(users)
            club = Club.objects.create(
                name=data['name'],
                description=data['description'],
                category=data['category'],
                email=f"{data['name'].lower().replace(' ', '')}@msu.ac.zw",
                website=f"https://clubs.msu.ac.zw/{data['name'].lower().replace(' ', '-')}",
                faculty_advisor=f'Dr. {random.choice(["Moyo", "Ncube", "Dube", "Sibanda", "Ndlovu", "Khumalo"])}',
                meeting_location=random.choice([
                    'Main Lecture Theatre', 'Science Block', 'Commerce Block',
                    'Student Center', 'Library Hall', 'Engineering Block',
                    'Kaguvi Hall', 'Nehanda Hall', 'Admin Block'
                ]),
                meeting_schedule=random.choice(['Monday 17:00', 'Wednesday 16:00', 'Friday 15:00', 'Thursday 17:30', 'Tuesday 16:30']),
                max_members=random.randint(50, 200),
                created_by=creator,
                is_active=True,
                is_approved=True,
                approved_by=creator,
                approved_at=timezone.now()
            )
            clubs.append(club)

        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(clubs)} clubs'))
        return clubs

    def create_churches(self, users):
        """Create sample churches."""
        self.stdout.write('Creating churches...')

        churches_data = [
            {'name': 'MSU Christian Union', 'denomination': 'other', 'description': 'Interdenominational fellowship for Christian students. Daily devotions and Bible studies.'},
            {'name': 'Catholic Society', 'denomination': 'catholic', 'description': 'Catholic students fellowship with weekly mass and prayer meetings.'},
            {'name': 'Seventh Day Adventist Fellowship', 'denomination': 'other', 'description': 'SDA students worship and fellowship every Sabbath.'},
            {'name': 'Methodist Society', 'denomination': 'methodist', 'description': 'Methodist students gathering for worship and community service.'},
            {'name': 'Pentecostal Students Fellowship', 'denomination': 'pentecostal', 'description': 'Spirit-filled worship, prayer meetings, and evangelism.'},
            {'name': 'Baptist Students Union', 'denomination': 'baptist', 'description': 'Baptist students fellowship with worship and discipleship programs.'},
            {'name': 'Scripture Union', 'denomination': 'other', 'description': 'Daily Bible reading, prayer groups, and evangelism training.'},
        ]

        churches = []
        for data in churches_data:
            creator = random.choice(users)
            church = Church.objects.create(
                name=data['name'],
                description=data['description'],
                denomination=data['denomination'],
                email=f"{data['name'].lower().replace(' ', '')}@msu.ac.zw",
                pastor_name=f'Pastor {random.choice(["Mpofu", "Ndlovu", "Moyo"])}',
                service_times=random.choice(['Sunday 09:00', 'Sunday 10:00', 'Sabbath 09:00']),
                contact_person=f'{random.choice(users).first_name} {random.choice(users).last_name}',
                phone_number=f'+263 77 {random.randint(100, 999)} {random.randint(1000, 9999)}',
                created_by=creator,
                is_active=True,
                is_approved=True,
                approved_by=creator,
                approved_at=timezone.now()
            )
            churches.append(church)

        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(churches)} churches'))
        return churches

    def create_sports_teams(self, users):
        """Create sample sports teams."""
        self.stdout.write('Creating sports teams...')

        teams_data = [
            {'name': 'MSU Football Team', 'sport': 'football', 'division': 'varsity', 'description': 'Varsity football team competing in university league.'},
            {'name': 'MSU Ladies Soccer', 'sport': 'football', 'division': 'varsity', 'description': 'Women\'s football team representing MSU in tournaments.'},
            {'name': 'Basketball Team', 'sport': 'basketball', 'division': 'varsity', 'description': 'Competitive basketball team for inter-university matches.'},
            {'name': 'Netball Team', 'sport': 'netball', 'division': 'varsity', 'description': 'MSU netball team competing at national level.'},
            {'name': 'Volleyball Squad', 'sport': 'volleyball', 'division': 'club', 'description': 'Indoor volleyball team for students of all skill levels.'},
            {'name': 'Athletics Club', 'sport': 'athletics', 'division': 'club', 'description': 'Track and field athletes training for competitions.'},
            {'name': 'Rugby Team', 'sport': 'rugby', 'division': 'varsity', 'description': 'MSU rugby team competing in Zimbabwe university league.'},
            {'name': 'Cricket Team', 'sport': 'cricket', 'division': 'club', 'description': 'Cricket team for friendly matches and tournaments.'},
            {'name': 'Chess Club', 'sport': 'other', 'division': 'recreational', 'description': 'Chess players of all levels welcome. Weekly tournaments.'},
        ]

        teams = []
        for data in teams_data:
            creator = random.choice(users)
            team = SportsTeam.objects.create(
                name=data['name'],
                description=data['description'],
                sport_type=data['sport'],
                division=data['division'],
                email=f"{data['name'].lower().replace(' ', '')}@msu.ac.zw",
                coach_name=f'Coach {random.choice(["Sibanda", "Khumalo", "Banda"])}',
                practice_schedule=random.choice([
                    'Mon/Wed/Fri 16:00',
                    'Tue/Thu 17:00',
                    'Weekend mornings'
                ]),
                home_venue=random.choice(['Main Field', 'Sports Complex', 'Indoor Arena']),
                season_start=timezone.now().date(),
                season_end=(timezone.now() + timedelta(days=180)).date(),
                created_by=creator,
                is_active=True,
                is_approved=True,
                approved_by=creator,
                approved_at=timezone.now()
            )
            teams.append(team)

        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(teams)} sports teams'))
        return teams

    def create_activities(self, users):
        """Create sample activities."""
        self.stdout.write('Creating activities...')

        activities_data = [
            {'name': 'Freshers Week 2024', 'type': 'social_event', 'description': 'Welcome event for new students with campus tours and social activities.'},
            {'name': 'Tech Hackathon', 'type': 'competition', 'description': '48-hour coding competition with prizes for innovative solutions.'},
            {'name': 'Career Fair', 'type': 'conference', 'description': 'Meet potential employers and learn about career opportunities.'},
            {'name': 'Mental Health Workshop', 'type': 'workshop', 'description': 'Interactive workshop on managing stress and mental wellness.'},
            {'name': 'Business Plan Competition', 'type': 'competition', 'description': 'Pitch your startup idea and win seed funding.'},
            {'name': 'Cultural Night', 'type': 'social_event', 'description': 'Celebrate diversity with music, dance, and traditional food.'},
            {'name': 'Blood Donation Drive', 'type': 'fundraiser', 'description': 'Partner with Red Cross for life-saving blood donations.'},
            {'name': 'Research Symposium', 'type': 'conference', 'description': 'Present your research and network with academics.'},
            {'name': 'Leadership Seminar', 'type': 'seminar', 'description': 'Develop leadership skills with industry experts.'},
            {'name': 'Sports Day', 'type': 'social_event', 'description': 'Inter-faculty sports competitions and fun activities.'},
        ]

        activities = []
        for i, data in enumerate(activities_data):
            creator = random.choice(users)
            start_date = timezone.now() + timedelta(days=random.randint(1, 90))

            activity = Activity.objects.create(
                name=data['name'],
                description=data['description'],
                activity_type=data['type'],
                location=random.choice(['Main Hall', 'Sports Complex', 'Library', 'Student Center', 'Online']),
                start_date=start_date,
                end_date=start_date + timedelta(hours=random.randint(2, 8)),
                registration_deadline=(start_date - timedelta(days=3)).date(),
                max_participants=random.randint(50, 300),
                is_recurring=False,
                created_by=creator,
                is_active=True,
                is_approved=True,
                approved_by=creator,
                approved_at=timezone.now()
            )
            activities.append(activity)

        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(activities)} activities'))
        return activities

    def create_memberships(self, users, clubs, churches, teams):
        """Create memberships."""
        self.stdout.write('Creating memberships...')

        membership_count = 0

        # Each user joins 2-5 clubs
        for user in users:
            user_clubs = random.sample(clubs, random.randint(2, min(5, len(clubs))))
            for club in user_clubs:
                ClubMembership.objects.create(
                    user=user,
                    club=club,
                    status='approved',
                    position='member',
                    joined_at=timezone.now() - timedelta(days=random.randint(1, 365)),
                    approved_at=timezone.now()
                )
                membership_count += 1

        # Each user might join 1 church
        for user in random.sample(users, int(len(users) * 0.6)):
            church = random.choice(churches)
            ChurchMembership.objects.create(
                user=user,
                church=church,
                status='approved',
                ministry=random.choice(['Choir', 'Ushering', 'Media', 'Prayer', 'Outreach']),
                joined_at=timezone.now() - timedelta(days=random.randint(1, 365))
            )
            membership_count += 1

        # Each user might join 1-2 sports teams
        for user in random.sample(users, int(len(users) * 0.4)):
            user_teams = random.sample(teams, random.randint(1, 2))
            for team in user_teams:
                SportsTeamMembership.objects.create(
                    user=user,
                    sports_team=team,
                    status='approved',
                    position=random.choice(['Player', 'Goalkeeper', 'Captain', 'Vice Captain']),
                    jersey_number=random.randint(1, 99),
                    joined_at=timezone.now() - timedelta(days=random.randint(1, 365)),
                    approved_at=timezone.now()
                )
                membership_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Created {membership_count} memberships'))

    def create_activity_registrations(self, users, activities):
        """Create activity registrations."""
        self.stdout.write('Creating activity registrations...')

        registration_count = 0
        for activity in activities:
            # Random number of users register for each activity
            participants = random.sample(users, random.randint(10, min(50, len(users))))
            for user in participants:
                ActivityRegistration.objects.create(
                    user=user,
                    activity=activity,
                    status='confirmed',
                    registered_at=timezone.now() - timedelta(days=random.randint(1, 30))
                )
                registration_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Created {registration_count} activity registrations'))

    def create_posts(self, users, clubs, churches, teams, activities):
        """Create posts."""
        self.stdout.write('Creating posts...')

        posts = []

        # Club posts
        for club in clubs:
            for _ in range(random.randint(2, 5)):
                post = Post.objects.create(
                    author=random.choice(users),
                    content_type=ContentType.objects.get_for_model(Club),
                    object_id=club.id,
                    post_type=random.choice(['announcement', 'event', 'recruitment', 'general']),
                    title=f'{club.name} - {random.choice(["Meeting", "Event", "Workshop", "Announcement"])}',
                    content=f'Important update from {club.name}. Join us for our upcoming activities!',
                    visibility='public',
                    is_pinned=random.choice([True, False]) if random.random() > 0.8 else False,
                    created_at=timezone.now() - timedelta(days=random.randint(1, 60))
                )
                posts.append(post)

        # Church posts
        for church in churches:
            for _ in range(random.randint(1, 3)):
                post = Post.objects.create(
                    author=random.choice(users),
                    content_type=ContentType.objects.get_for_model(Church),
                    object_id=church.id,
                    post_type=random.choice(['announcement', 'event', 'general']),
                    title=f'{church.name} - {random.choice(["Service", "Prayer Meeting", "Bible Study"])}',
                    content=f'Fellowship update from {church.name}. God bless!',
                    visibility='public',
                    created_at=timezone.now() - timedelta(days=random.randint(1, 60))
                )
                posts.append(post)

        # Sports team posts
        for team in teams:
            for _ in range(random.randint(1, 4)):
                post = Post.objects.create(
                    author=random.choice(users),
                    content_type=ContentType.objects.get_for_model(SportsTeam),
                    object_id=team.id,
                    post_type=random.choice(['achievement', 'event', 'announcement']),
                    title=f'{team.name} - {random.choice(["Match", "Training", "Victory", "Tournament"])}',
                    content=f'Latest from {team.name}. Come support your team!',
                    visibility='public',
                    created_at=timezone.now() - timedelta(days=random.randint(1, 60))
                )
                posts.append(post)

        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(posts)} posts'))
        return posts

    def create_engagement(self, users, posts):
        """Create likes, comments, and shares."""
        self.stdout.write('Creating engagement...')

        likes_count = 0
        comments_count = 0
        shares_count = 0

        for post in posts:
            # Likes (20-80% of users like each post)
            likers = random.sample(users, random.randint(int(len(users) * 0.2), int(len(users) * 0.8)))
            for user in likers:
                PostLike.objects.create(post=post, user=user)
                likes_count += 1
            post.likes_count = len(likers)

            # Comments (10-30% of users comment)
            commenters = random.sample(users, random.randint(int(len(users) * 0.1), int(len(users) * 0.3)))
            for user in commenters:
                PostComment.objects.create(
                    post=post,
                    user=user,
                    content=random.choice([
                        'Great initiative!',
                        'Looking forward to this!',
                        'Count me in!',
                        'This is amazing!',
                        'When is the next meeting?',
                        'Thanks for sharing!',
                    ])
                )
                comments_count += 1
            post.comments_count = len(commenters)

            # Shares (5-15% of users share)
            sharers = random.sample(users, random.randint(int(len(users) * 0.05), int(len(users) * 0.15)))
            for user in sharers:
                PostShare.objects.create(
                    post=post,
                    user=user,
                    comment='Check this out!'
                )
                shares_count += 1
            post.shares_count = len(sharers)

            post.save()

        self.stdout.write(self.style.SUCCESS(f'✅ Created {likes_count} likes, {comments_count} comments, {shares_count} shares'))

    def populate_search_index(self, clubs, churches, teams, activities):
        """Populate search index."""
        self.stdout.write('Populating search index...')

        for club in clubs:
            SearchIndex.objects.create(
                organization_type='club',
                organization_id=club.id,
                name=club.name,
                description=club.description,
                category=club.category,
                is_active=club.is_active,
                is_approved=club.is_approved,
                member_count=club.clubmembership_set.count()
            )

        for church in churches:
            SearchIndex.objects.create(
                organization_type='church',
                organization_id=church.id,
                name=church.name,
                description=church.description,
                category=church.denomination,
                is_active=church.is_active,
                is_approved=church.is_approved,
                member_count=church.churchmembership_set.count()
            )

        for team in teams:
            SearchIndex.objects.create(
                organization_type='sports_team',
                organization_id=team.id,
                name=team.name,
                description=team.description,
                category=team.sport_type,
                is_active=team.is_active,
                is_approved=team.is_approved,
                member_count=team.sportsteammembership_set.count()
            )

        for activity in activities:
            SearchIndex.objects.create(
                organization_type='activity',
                organization_id=activity.id,
                name=activity.name,
                description=activity.description,
                category=activity.activity_type,
                is_active=activity.is_active,
                is_approved=activity.is_approved,
                member_count=activity.activityregistration_set.count()
            )

        self.stdout.write(self.style.SUCCESS(f'✅ Populated search index'))

    def display_summary(self):
        """Display summary of created data."""
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('MSU Gweru Campus - Sample Data Population Complete!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f'\n  👥 Users: {User.objects.count()} (MSU Gweru students)')
        self.stdout.write(f'  🎓 Clubs: {Club.objects.count()}')
        self.stdout.write(f'  ⛪ Churches: {Church.objects.count()}')
        self.stdout.write(f'  ⚽ Sports Teams: {SportsTeam.objects.count()}')
        self.stdout.write(f'  📅 Activities: {Activity.objects.count()}')
        self.stdout.write(f'  📝 Posts: {Post.objects.count()}')
        self.stdout.write(f'  ❤️  Likes: {PostLike.objects.count()}')
        self.stdout.write(f'  💬 Comments: {PostComment.objects.count()}')
        self.stdout.write(f'  🔄 Shares: {PostShare.objects.count()}')
        self.stdout.write(f'  🔍 Search Index: {SearchIndex.objects.count()}\n')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('\n✨ Midlands State University Gweru Campus platform is ready!'))
        self.stdout.write(self.style.SUCCESS('   All data reflects MSU Gweru structure and culture.'))
        self.stdout.write(self.style.SUCCESS('=' * 70 + '\n'))
