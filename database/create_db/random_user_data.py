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


faculty = random.choice(["İnsaat Fakültesi", "Mimarlik Fakültesi", "Makina Fakültesi", "Elektrik-Elektronik Fakültesi", "Denizcilik Fakültesi", "Kimya-Metalurji Fakültesi",
                            "İşletme Fakültesi", "Ucak ve Uzay Bilimleri Fakültesi", "Tekstil Teknolojileri ve Tasarim Fakültesi", "Maden Fakültesi",
                            "Gemi Insaati ve Deniz Bilimleri Fakültesi", "Bilgisayar ve Bilisim Fakültesi", "Fen-Edebiyat Fakültesi"])

faculty_dict = {
    "İnşaat Fakültesi" : np.random.choice(["İnşaat Mühendisliği", "Geomatik Mühendisliği", "Çevre Mühendisliği"]),
    "Mimarlık Fakültesi" : np.random.choice(["Mimarlık", "Şehir ve Bölge Planlama", "Endüstri Ürünleri Tasarımı", "Endüstriyel Tasarım", "İç Mimarlık", "Peyzaj Mimarlığı"]),
    "Makina Fakültesi" : np.random.choice(["Makina Mühendisliği", "İmalat Mühendisliği"]),
    "Elektrik-Elektronik Fakültesi" : np.random.choice(["Elektronik ve Haberleşme Mühendisliği", "Elektrik Mühendisliği", "Elektronik Mühendisliği", "Telekomünikasyon Mühendisliği", "Kontrol ve Otomasyon Mühendisliği"]),
    "Maden Fakültesi" : np.random.choice(["Jeoloji Mühendisliği", "Jeofizik Mühendisliği", "Maden Mühendisliği", "Petrol ve Doğal Gaz Mühendisliği", "Cevher Hazırlama Mühendisliği"]),
    "Kimya - Metalurji Fakültesi" : np.random.choice(["Kimya Mühendisliği", "Gıda Mühendisliği", "Metalurji ve Malzeme Mühendisliği"]),
    "İşletme Fakültesi" : np.random.choice(["İşletme Mühendisliği", "Endüstri Mühendisliği", "Ekonomi"]),
    "Gemi İnşaatı ve Deniz Bilimleri Fakültesi" : np.random.choice(["Gemi ve Deniz Teknolojisi Mühendisliği", "Gemi İnşaatı ve Gemi Makineleri Mühendisliği"]),
    "Fen - Edebiyat Fakültesi" : np.random.choice(["Matematik Mühendisliği", "Fizik Mühendisliği", "Kimya", "Moleküler Biyoloji ve Genetik"]),
    "Uçak ve Uzay Bilimleri Fakültesi" : np.random.choice(["Meteoroloji Mühendisliği", "Uzay Mühendisliği", "Uçak Mühendisliği"]),
    "Denizcilik Fakültesi" : np.random.choice(["Deniz Ulaştırma İşletme Mühendisliği", "Gemi Makinaları İşletme Mühendisliği"]),
    "Tekstil Teknolojileri ve Tasarımı Fakültesi" : np.random.choice(["Tekstil Mühendisliği"]),
    "Bilgisayar ve Bilişim Fakültesi" : np.random.choice(["Bilgisayar Mühendisliği", "Yapay Zeka ve Veri Mühendisliği"])
    }

def get_random_faculty_department(faculty, faculty_dict):

    fac = faculty
    dep = faculty_dict[fac]
    
    
    return fac, dep





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
