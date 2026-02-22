#!/usr/bin/env python3
"""Seed DynamoDB with initial page content."""
import boto3
import sys
import json

TABLE_NAME = sys.argv[1] if len(sys.argv) > 1 else 'dev-rozellerz-pages'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

PAGES = [
    {
        'slug': 'rohit',
        'title': 'rohit',
        'subtitle': 'engineer',
        'sort_order': 1,
        'tags': ['Python', 'JavaScript', 'AWS', 'Web Development', 'Automation'],
        'body': '<p>The destination — and the starting point. Everything on this map connects back here. Engineer, creator, builder.</p><h3>The Thread</h3><p>From data to design to art, it\'s all the same impulse: take something complex, understand it deeply, and make something new from it.</p><h3>Connect</h3><p>rozellerz.com</p>',
    },
    {
        'slug': 'data-engineer',
        'title': 'data engineer',
        'subtitle': 'engineering',
        'sort_order': 2,
        'tags': ['SQL', 'Python', 'AWS', 'Spark', 'Airflow'],
        'body': '<p>Building the pipelines and infrastructure that turn raw data into something usable. The backbone of every data-driven decision.</p><h3>Focus Areas</h3><p>ETL pipelines, data modeling, cloud infrastructure, and making sure the right data gets to the right place at the right time.</p>',
    },
    {
        'slug': 'data-analyst',
        'title': 'data analyst',
        'subtitle': 'data engineer',
        'sort_order': 3,
        'tags': ['Pandas', 'SQL', 'Tableau', 'Excel', 'Statistics'],
        'body': '<p>Finding the story inside the numbers. Data analysis is where engineering meets intuition — pattern recognition at scale.</p><h3>Approach</h3><p>Ask the right questions, explore the data, visualize the patterns, and communicate findings that actually drive action.</p>',
    },
    {
        'slug': 'designer',
        'title': 'designer',
        'subtitle': 'design engineer',
        'sort_order': 4,
        'tags': ['Figma', 'CSS', 'SVG', 'Typography', 'Motion'],
        'body': '<p>Where engineering meets aesthetics. Design isn\'t just how it looks — it\'s how it works, how it feels, and how it communicates.</p><h3>Philosophy</h3><p>Every pixel has a purpose. Clean, intentional design that respects the user and serves the content. Less decoration, more communication.</p>',
    },
    {
        'slug': 'art',
        'title': 'art',
        'subtitle': 'rz flow',
        'sort_order': 5,
        'tags': ['Music Production', 'Stand-Up Comedy', 'Creative Writing', 'Visual Art'],
        'body': '<p>The creative layer. Art is where rules break down and expression takes over — music, comedy, visual experiments, and everything in between.</p><h3>Creative Work</h3><p>Stand-up comedy writing, music production, type beats, creative writing — art is the outlet that feeds everything else.</p>',
    },
    {
        'slug': 'rozelle',
        'title': 'rozelle',
        'subtitle': 'designer',
        'sort_order': 6,
        'tags': ['Python', 'JavaScript', 'AWS', 'Web Development', 'Automation'],
        'body': '<p>The origin point. Rozelle is where it all starts — a foundation built on curiosity, problem-solving, and building things from scratch.</p><h3>About</h3><p>This is the hub that connects every discipline on this map. Engineering isn\'t just code — it\'s a way of thinking about systems, creativity, and making ideas real.</p>',
    },
]


def seed():
    print(f'Seeding table: {TABLE_NAME}')
    for page in PAGES:
        table.put_item(Item=page)
        print(f'  ✓ {page["slug"]}')
    print(f'Done — {len(PAGES)} pages seeded.')


if __name__ == '__main__':
    seed()
