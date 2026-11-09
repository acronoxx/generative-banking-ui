"""HTTP routes, mounted under /api by app/main.py.

Each route gets the database session and the connected user (from the
Authorization header) as FastAPI dependencies, then calls a service of app/services/.
"""
