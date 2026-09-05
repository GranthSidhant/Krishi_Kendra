import sys
from app import create_app
from app.models import User
from seed.sample_data import seed_all_sample_data

app = create_app()

@app.cli.command("seed")
def seed_command():
    """Seeds the database with sample demonstration data."""
    seed_all_sample_data(app)
    print("Database seeded successfully via CLI.")

if __name__ == '__main__':
    # Check if DB is empty, auto-seed for instant demo readiness
    with app.app_context():
        if User.query.count() == 0:
            print("Empty database detected. Auto-seeding sample data for Krishi Kendra...")
            seed_all_sample_data(app)

    if len(sys.argv) > 1 and sys.argv[1] == 'seed':
        with app.app_context():
            seed_all_sample_data(app)
    else:
        print("Starting Krishi Kendra web server at http://127.0.0.1:5000 ...")
        app.run(host='0.0.0.0', port=5000, debug=True)
