# FoodSpot

A Django-based platform to discover, view, and interact with restaurants — bookmark favorites, mark visits, and leave ratings & reviews.

## Setup

1. Clone the repo
```bash
   git clone https://github.com/<your-username>/foodspot-django.git
   cd foodspot-django
```

2. Create and activate a virtual environment
```bash
   python -m venv venv
   source venv/bin/activate   
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Run migrations
```bash
   python manage.py migrate
```

5. Start the development server
```bash
   python manage.py runserver
```