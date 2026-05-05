# MSU Gweru Campus - Sample Data Guide

**Specifically designed for Midlands State University Gweru Campus, Zimbabwe**

---

## 📋 Overview

This guide explains the sample data population command that creates realistic test data for the MSU Platform, specifically tailored to **Midlands State University (MSU) Gweru Campus** in Zimbabwe.

---

## 🎯 Purpose

The `populate_sample_data` management command creates a fully functional test environment that reflects the actual structure and culture of MSU Gweru, including:

- **Authentic Zimbabwean context**: Names, email addresses, and cultural references
- **MSU Gweru structure**: 9 faculties, campus buildings, and organizations
- **Realistic engagement**: Posts, likes, comments, and shares that mirror actual student behavior
- **Campus culture**: Organizations, events, and activities typical of MSU Gweru

---

## 🏛️ MSU Gweru Structure

### Faculties (9 Total)

Based on MSU Gweru's actual faculty structure:

1. **Agriculture** - Agricultural sciences and management
2. **Arts** - Humanities, languages, and creative arts
3. **Commerce** - Business, accounting, economics
4. **Education** - Teacher training and educational studies
5. **Engineering** - Civil, mechanical, and other engineering disciplines
6. **Law** - Legal studies and practice
7. **Science and Technology** - Computer science, mathematics, physics, chemistry, IT
8. **Social Sciences** - Psychology, sociology, development studies
9. **Medicine** - Medical and health sciences

### Campus Locations

Sample data uses authentic MSU Gweru campus locations:

- **Main Lecture Theatre** - Central teaching facility
- **Science Block** - Science and Technology faculty building
- **Commerce Block** - Commerce faculty building
- **Engineering Block** - Engineering faculty building
- **Student Center** - Social and recreational hub
- **Library Hall** - Academic resource center
- **Admin Block** - Administrative offices
- **Kaguvi Hall** - Student residence (named after Zimbabwean anti-colonial hero)
- **Nehanda Hall** - Student residence (named after Zimbabwean anti-colonial heroine)
- **Main Field** - Outdoor sports facility
- **Sports Complex** - Indoor and outdoor sports facilities
- **Indoor Arena** - Indoor sports and events venue

---

## 👥 Sample Data Created

### Users (Default: 50, Configurable)

**Authentic Zimbabwean Names:**
- First names: Tanaka, Rumbi, Tinashe, Chipo, Tendai, Rudo, Tariro, Nyasha, Blessing, Takudzwa, etc.
- Last names: Moyo, Ncube, Sibanda, Dube, Ndlovu, Mpofu, Khumalo, Nkomo, Nyathi, etc.

**Student Details:**
- Email: `firstname.lastname@msu.ac.zw`
- Student Number: `MSU2020-2024[random]` (e.g., MSU20243456)
- Faculty: Random from 9 MSU Gweru faculties
- Department: Relevant to faculty
- Year of Study: 1-4
- All users verified and active

### Clubs (21 Total)

**Technology Clubs (4):**
1. MSU Tech Society - Technology, coding, innovation
2. Computer Science Club - Programming, competitions, lectures
3. Web Developers Association - Web development, projects
4. Data Science Society - Data analytics, ML, AI

**Academic Clubs (5):**
5. Debate Society - Critical thinking, public speaking
6. Law Students Association - Moot courts, legal aid
7. Business Club - Entrepreneurship, competitions
8. Economics Society - Economic theory, guest speakers
9. Science Club - Experiments, science fairs

**Cultural & Arts Clubs (5):**
10. Drama Society - Plays, musicals, theatre
11. Music Club - Musicians, jam sessions, concerts
12. Poetry Society - Open mic, poetry slams
13. Photography Club - Photo walks, exhibitions
14. Cultural Heritage Society - Zimbabwean culture, dance, music

**Volunteer & Social Clubs (3):**
15. Environmental Club - Clean-ups, tree planting
16. Red Cross Society - First aid, blood drives
17. Rotaract Club - Community service, leadership

**Professional Clubs (4):**
18. AIESEC MSU - Global internships, exchanges
19. Marketing Society - Case competitions, career workshops
20. Accountants Club - Exam prep, career guidance
21. Engineering Society - Technical workshops, competitions

**Each Club Includes:**
- Name and description
- Category (technology, academic, arts, volunteer, professional, cultural)
- Email: `clubname@msu.ac.zw`
- Website: `https://clubs.msu.ac.zw/club-name`
- Faculty Advisor: Dr. [Zimbabwean surname]
- Meeting Location: Campus building
- Meeting Schedule: Weekday evening times
- Max Members: 50-200

### Churches (7 Total)

Religious organizations reflecting Zimbabwe's Christian culture:

1. **MSU Christian Union** - Interdenominational fellowship
2. **Catholic Society** - Catholic students, weekly mass
3. **Seventh Day Adventist Fellowship** - SDA worship
4. **Methodist Society** - Methodist worship and service
5. **Pentecostal Students Fellowship** - Spirit-filled worship
6. **Baptist Students Union** - Baptist fellowship
7. **Scripture Union** - Bible reading, evangelism

**Each Church Includes:**
- Denomination
- Service times (Sunday or Sabbath)
- Pastor/leader name
- Contact person
- Phone number: +263 77 XXX XXXX (Zimbabwean mobile format)

### Sports Teams (9 Total)

1. **MSU Football Team** - Varsity men's football
2. **MSU Ladies Soccer** - Varsity women's football
3. **Basketball Team** - Varsity basketball
4. **Netball Team** - Varsity netball (popular in Zimbabwe)
5. **Volleyball Squad** - Club volleyball
6. **Athletics Club** - Track and field
7. **Rugby Team** - Varsity rugby
8. **Cricket Team** - Club cricket
9. **Chess Club** - Recreational chess

**Each Team Includes:**
- Sport type and division (varsity/club/recreational)
- Coach name
- Practice schedule
- Home venue (Main Field, Sports Complex, Indoor Arena)
- Season dates

### Activities (10 Total)

Campus events and activities:

1. **Freshers Week 2024** - Welcome event for new students
2. **Tech Hackathon** - 48-hour coding competition
3. **Career Fair** - Meet employers, career opportunities
4. **Mental Health Workshop** - Stress management, wellness
5. **Business Plan Competition** - Startup pitches, seed funding
6. **Cultural Night** - Diversity celebration, music, dance, food
7. **Blood Donation Drive** - Red Cross partnership
8. **Research Symposium** - Present research, networking
9. **Leadership Seminar** - Leadership skills development
10. **Sports Day** - Inter-faculty sports competitions

**Each Activity Includes:**
- Activity type (competition, workshop, seminar, conference, social event, fundraiser)
- Location
- Start and end dates
- Registration deadline
- Max participants: 50-300

### Memberships

**Realistic Distribution:**
- Each user joins 2-5 clubs
- 60% of users join 1 church
- 40% of users join 1-2 sports teams
- Each activity has random registrations

**Membership Details:**
- Status: Approved
- Position: Member, Captain, Vice Captain (for sports)
- Ministry: Choir, Ushering, Media, Prayer, Outreach (for churches)
- Jersey Number: 1-99 (for sports)
- Join date: Random within past year

### Posts

**Volume:**
- 2-5 posts per club
- 1-3 posts per church
- 1-4 posts per sports team
- 1-2 posts per activity

**Post Types:**
1. **Announcement** - Important updates
2. **Event** - Upcoming events
3. **Achievement** - Success stories, awards
4. **General** - General discussions
5. **Media** - Photos, videos
6. **Recruitment** - Member recruitment

**Post Features:**
- Title and content
- Author (random member)
- Post type and visibility (public, members, private)
- Some posts pinned
- Created 1-90 days ago

### Engagement

**Likes:**
- 30-70% of users like each post
- Realistic like counts

**Comments:**
- 10-30% of users comment on each post
- Thoughtful comment content
- Some replies to comments (nested comments)

**Shares:**
- 5-15% of users share posts
- Optional share comments

### Search Index

All organizations automatically indexed for search functionality:
- Clubs, churches, sports teams, activities
- Searchable by name, description, category
- Member counts included
- Active status tracked

---

## 🚀 Usage

### Basic Command

```bash
# Default: Creates 50 users and all sample data
python manage.py populate_sample_data
```

### With Options

```bash
# Clear existing data first
python manage.py populate_sample_data --clear

# Create 100 users instead of 50
python manage.py populate_sample_data --users 100

# Clear and create 100 users
python manage.py populate_sample_data --clear --users 100
```

### Docker Usage

```bash
# Default
docker-compose exec web python manage.py populate_sample_data

# With options
docker-compose exec web python manage.py populate_sample_data --clear --users 100
```

---

## 📊 Expected Output

```
======================================================================
Midlands State University Gweru Campus
Sample Data Population
======================================================================

Creating users...
✅ Created 50 users
Creating clubs...
✅ Created 21 clubs
Creating churches...
✅ Created 7 churches
Creating sports teams...
✅ Created 9 sports teams
Creating activities...
✅ Created 10 activities
Creating memberships...
✅ Created [X] memberships
Creating activity registrations...
✅ Created [X] activity registrations
Creating posts...
✅ Created [X] posts
Creating engagement...
✅ Created [X] likes, [X] comments, [X] shares
✅ Populated search index

======================================================================
MSU Gweru Campus - Sample Data Population Complete!
======================================================================

  👥 Users: 50 (MSU Gweru students)
  🎓 Clubs: 21
  ⛪ Churches: 7
  ⚽ Sports Teams: 9
  📅 Activities: 10
  📝 Posts: [X]
  ❤️  Likes: [X]
  💬 Comments: [X]
  🔄 Shares: [X]
  🔍 Search Index: 47

======================================================================
✨ Midlands State University Gweru Campus platform is ready!
   All data reflects MSU Gweru structure and culture.
======================================================================
```

---

## 🎓 MSU Gweru Context

### Why This Matters

This sample data is specifically designed for **Midlands State University Gweru Campus** to ensure:

1. **Authenticity**: Uses actual MSU Gweru structure (9 faculties, campus buildings)
2. **Cultural Accuracy**: Zimbabwean names, phone formats, cultural context
3. **Realistic Testing**: Data mirrors actual student organization patterns
4. **Easy Demonstration**: Show platform features with familiar context
5. **Training**: Help MSU Gweru staff learn the system with relevant examples

### Data Sources

Sample data based on research from:
- [Midlands State University official website](https://ww5.msu.ac.zw)
- [MSU Wikipedia article](https://en.wikipedia.org/wiki/Midlands_State_University)
- [University of Zimbabwe (comparison)](https://www.uz.ac.zw)
- [Africa University clubs (comparison)](https://africau.edu)
- General knowledge of Zimbabwean university culture

### What's Included

✅ **Accurate**:
- 9 MSU Gweru faculties
- MSU email format (@msu.ac.zw)
- Zimbabwean names and surnames
- Campus building names (Kaguvi Hall, Nehanda Hall - named after Zimbabwean heroes)
- Zimbabwean phone number format (+263 77 XXX XXXX)
- Cultural context (churches, sports, clubs typical of Zimbabwean universities)

✅ **Realistic**:
- Student numbers (MSU prefix)
- Organization types common at MSU
- Meeting locations and schedules
- Faculty advisors with Zimbabwean names
- Event types typical of campus life

---

## 🔒 Security Notes

### Default Passwords

**⚠️ IMPORTANT**: All sample users are created with password `password123`

**For Production:**
1. Never use this command in production with real users
2. Change default passwords if using sample users for demos
3. Consider deleting sample users before going live
4. Use `--clear` flag to remove all sample data

### Sample Data Scope

This command only creates:
- Non-superuser accounts
- Sample organizations and content
- Test engagement data

It does NOT:
- Modify existing superuser accounts
- Change system settings
- Affect production data (if run with `--clear`, only removes sample data)

---

## 🧹 Cleaning Up

### Clear All Sample Data

```bash
# Clears all users (except superusers), organizations, posts, etc.
python manage.py populate_sample_data --clear
```

This removes:
- All non-superuser accounts
- All clubs, churches, sports teams, activities
- All posts, likes, comments, shares
- Search index entries

**Preserves:**
- Superuser accounts
- Database schema
- System settings

---

## 📚 Related Documentation

- **README.md** - Project overview
- **DEPLOY.md** - Deployment guide
- **IMPLEMENTATION_COMPLETE.md** - Feature completion summary
- **PROJECT_STATUS.md** - Current project status

---

## 🤝 Contributing

To add more MSU Gweru-specific data:

1. Research actual MSU Gweru organizations
2. Update `clubs_data`, `churches_data`, `teams_data`, or `activities_data` lists
3. Ensure names, locations, and context are authentic
4. Test the command after changes

---

## 💬 Support

For questions about MSU Gweru sample data:

- Check documentation files
- Review command output for statistics
- Test in development environment first
- Verify data accuracy with MSU Gweru staff

---

**🚀 Ready to populate your MSU Gweru Campus platform with realistic data!**

---

*Last Updated: May 5, 2026*
*Version: 1.0*
*Specifically for: Midlands State University Gweru Campus, Zimbabwe*
