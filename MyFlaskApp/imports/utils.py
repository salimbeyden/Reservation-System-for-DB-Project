from MyFlaskApp import mysql

def manipulate_hist_data(data, type):
    if type == "ind":
        
        title = ["First Player", "Score", "Second Player", "Campus", "Facility", "Sport", "Date"]

        hists = list()
        for row in data:
            hist = dict()

            hist["u1_name"] = f"{row[0]} {row[1]}".title()
            hist["u1_id"] = row[2]
            hist["score"] = f"{row[3]} - {row[4]}"
            hist["u2_name"] = f"{row[5]} {row[6]}".title()
            hist["u2_id"] = row[7]
            hist["campus_name"] = row[8]
            hist["campus_id"] = row[9]
            hist["facility_name"] = row[10].split(" ")[0]
            hist["facility_id"] = row[11]
            hist["sport_type"] = row[12]
            hist["sport_id"] = row[13]
            hist["date"] = row[14]

            hists.append(hist)
        

    return hists ,title

def manipulate_rank_data(data):
    title = ["Team name", "Captain", "Sport", "Total Score", "Total matches", "Average Score", "Foundation Date"]

    teams = list()

    for row in data:
        team = dict()

        team["name"] = row[0].title()
        team["team_id"] = row[1]
        team["captain"] = f"{row[2]} {row[3]}".title()
        team["captain_id"] = row[4]
        team["sport"] = row[5].split(" ")[0]
        team["sport_id"] = row[6]
        team["#_matches"] = row[7]
        team["total_score"] = row[8]
        team["avrg_score"] = round(row[9], 1)
        team["foundation_date"] = row[10]

        teams.append(team)

    return teams, title

def manipulate_team_info(data):
    data = data[0]

    team = dict()

    team["name"] = data[0].title()
    team["team_id"] = data[1]
    team["captain"] = data[2].capitalize() + " " + data[3].capitalize()
    team["captain_id"] = data[4]
    team["sport_type"] = data[5]
    team["sport_id"] = data[6]
    team["fuoundation_date"] = data[7]
    team["team_score"] = data[8]
    team["capacity_max"] = data[9]
    team["#_matches"] = data[10]
    team["avrg"] = round(int(data[8]) / int(data[10]), 2)

    return team

def manipulate_profile_teams(data, user_id):

    teams = list()

    for row in data:
        team = dict()

        team["name"] = row[0].title()
        team["team_id"] = row[1]
        team["team_score"] = row[2]
        team["sport_type"] = row[3]
        team["sport_id"] = row[4]
        team["captain_id"] = row[5]
        team["name"] += " (C)" if team["captain_id"] == int(user_id) else ""
        
        teams.append(team)

    return teams

def manipulate_profile_user(data):
    data = data[0]
    user = dict()

    user["name"] = f"{data[0]} {data[1]}".title()
    user["school_id"] = str(data[2])
    user["mail"] = data[3]
    user["tel_no"] = data[4]
    user["faculty"] = data[5]
    user["department"] = data[6]
    user["birth_date"] = data[7]
    user["gender"] = data[8]

    return user

def manipulate_facility_info(data):
    facility = dict()

    facility["facility_id"] = data[0]
    facility["name"] = data[1]
    facility["campus_id"] = data[2]
    facility["tel_no"] = data[3]
    facility["email"] = data[4]
    facility["address"] = data[5]

    return facility

def manipulate_campus_info(data):
    campus = dict()

    campus["campus_id"] = data[0]
    campus["name"] = data[1]
    campus["address"] = data[2]

    return campus

def manipulate_campus_dropdown():
    cursor = mysql.connection.cursor()
    
    # to get campus names
    cursor.execute("SELECT * FROM campus")
    campuses = cursor.fetchall()
    cursor.close()
    
    campus_dropdown = [{"id": campus[0], "name": campus[1]} for campus in campuses]
    return campus_dropdown

def manipulate_sports_dropdown():
    cursor = mysql.connection.cursor()
    
    # to get sports names
    cursor.execute("SELECT * FROM sport")
    sports = cursor.fetchall()
    cursor.close()
    
    sports_dropdown = [{"id": sport[0], "name": sport[1]} for sport in sports]
    return sports_dropdown

def manipulate_reservation_data(data):

    title = ['Campus', 'Saloon', 'Sport', 'Mail Address']

    rows = list()

    for row in data:
        line = dict()

        line['campus'] = row[0]
        line['saloon'] = row[1]
        line['sport'] = row[2]
        line['mail'] = row[3]

        rows.append(line)
    
    return rows, title
