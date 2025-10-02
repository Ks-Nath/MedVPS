import sqlite3

# Connect to the same database
conn = sqlite3.connect("data/analytics.sqlite")
c = conn.cursor()

# Query unique visitors per page
c.execute("SELECT page, COUNT(session_id) FROM page_views GROUP BY page")
rows = c.fetchall()

# Print results
for p, count in rows:
    print(f"{p.replace('_', ' ').title()}: {count} unique visitors")
