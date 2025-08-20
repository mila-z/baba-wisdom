# Baba Wisdom

A web app where users can share, view, and search wisdom, with roles like admin, baba, and apprentice.

## Table of Contents 
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Technologies](#technologies)

## Installation
1. Clone the repo:
```bash
git clone https://github.com/mila-z/baba-wisdom.git
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Set environmental variables if needed
4. Run the app:
```bash
python main.py
```

## Usage
- Navigate to `/` for the homepage.
- Admins can view statistics such as what are the distinct villages and how many babas from there are registered, how many stars each baba has under all of her wisdom combined, what are the distinct categories and how many wisdom entries contain them.
- Babas can post, delete, search and view wisdom.
- Apprentices can search, view and leave a comment under a wisdom.

## Features 
- User registration and login.
- Role-based access (admin, baba, apprentice)
- Post, view, search wisdom
- Account deletion

## Technologies
- Python, Flask
- SQLAlchemy
- SQLite
- HTML, CSS, JavaScript