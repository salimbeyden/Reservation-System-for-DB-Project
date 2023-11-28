import random
from faker import Faker

fake = Faker()

# Random kullanıcı sayısı
user_count = 100

#random sport id
def get_random_sport_id():
    # Spor tablosundan rastgele bir sport_id seç
    result = random.choice([1, 2, 3, 4, 5, 6, 7])
    return result

def get_random_faculty_department():
    faculty = random.choice(["İnsaat Fakültesi", "Mimarlik Fakültesi", "Makina Fakültesi", "Elektrik-Elektronik Fakültesi", "Denizcilik Fakültesi", "Kimya-Metalurji Fakültesi",
                            "İşletme Fakültesi", "Ucak ve Uzay Bilimleri Fakültesi", "Tekstil Teknolojileri ve Tasarim Fakültesi", "Maden Fakültesi",
                            "Gemi Insaati ve Deniz Bilimleri Fakültesi", "Bilgisayar ve Bilisim Fakültesi", "Fen-Edebiyat Fakültesi"])
    

    if(faculty = "İnsaat Fakültesi"):
        department = random.choice([])
    elif(faculty = "Mimarlik Fakültesi"):
        department = random.choice([])
    elif(faculty = "Makina Fakültesi"):
        department = random.choice([])
    elif(faculty = "Makina Fakültesi"):
        department = random.choice([])
    elif(faculty = "Elektrik-Elektronik Fakültesi"):
        department = random.choice([])
    elif(faculty = "Denizcilik Fakültesi"):
        department = random.choice([])
    elif(faculty = "Kimya-Metalurji Fakültesi"):
        department = random.choice([])
    elif(faculty = "İşletme Fakültesi"):
        department = random.choice([])
    elif(faculty = "Ucak ve Uzay Bilimleri Fakültesi"):
        department = random.choice([])
    elif(faculty = "Tekstil Teknolojileri ve Tasarim Fakültesi"):
        department = random.choice([])
    elif(faculty = "Maden Fakültesi"):
        department = random.choice([])
    elif(faculty = "Gemi Insaati ve Deniz Bilimleri Fakültesi"):
        department = random.choice([])
    elif(faculty = "Bilgisayar ve Bilisim Fakültesi"):
        department = random.choice([])
    else:
        #fen edebiyat bölümleri
        department = random.choice([])
    return faculty, department





# Kullanıcı tablosu oluşturma
users = []
for _ in range(user_count):
    user = {
        'school_id': fake.uuid4(),
        'name': fake.first_name(),
        'surname': fake.last_name(),
        'mail': fake.email(),
        'tel_no': fake.phone_number(),
        'faculty_name': get_random_faculty_department()[0],
        'department': get_random_faculty_department()[1],
        'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=30),
        'password': fake.password(),
        'gender': fake.random_element(elements=('Male', 'Female')),
        'futbol_team_id': get_random_sport_id(),
        'voleybol_team_id': get_random_sport_id(),
        'basketbol_team_id': get_random_sport_id(),
        'tennis_team_id': get_random_sport_id(),
        'ping_pong_team_id': get_random_sport_id(),
    }
    users.append(user)


"""
kullanıcı verilerini tabloya eklemek için kullanılacak statementin taslağı
"""
for user in users:
    insert_query = '''
        INSERT INTO users (
            school_id, name, surname, mail, tel_no, faculty_name, department, birth_date,
            password, gender, futbol_team_id, voleybol_team_id, basketbol_team_id,
            tennis_team_id, ping_pong_team_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (
        user['school_id'], user['name'], user['surname'], user['mail'], user['tel_no'],
        user['faculty_name'], user['department'], user['birth_date'], user['password'],
        user['gender'], user['futbol_team_id'], user['voleybol_team_id'],
        user['basketbol_team_id'], user['tennis_team_id'], user['ping_pong_team_id']
    )
    cursor.execute(insert_query, data)
