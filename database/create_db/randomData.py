from faker import Faker
import random

fake = Faker()

# Generate random data for the User table
def generate_user_data():
    data = {
        'school_id': fake.random_int(min=1000, max=9999),
        'name': fake.first_name(),
        'surname': fake.last_name(),
        'mail': fake.email(),
        'tel_no': fake.phone_number(),
        'faculty_name': fake.word(),
        'department': fake.word(),
        'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=50),
        'password': fake.password(),
        'gender': random.choice(['Male', 'Female']),
        'futbol_team_id': fake.random_int(min=1, max=100),
        'voleybol_team_id': fake.random_int(min=1, max=100),
        'basketbol_team_id': fake.random_int(min=1, max=100),
        'tennis_team_id': fake.random_int(min=1, max=100),
        'ping_pong_team_id': fake.random_int(min=1, max=100),
    }
    return data



# Example: Generate and print data for 10 users
for _ in range(10):
    user_data = generate_user_data()
    print(user_data)
