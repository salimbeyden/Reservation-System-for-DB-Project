from MyFlaskApp import mysql

def manipulate_hist_data(data, is_ind):
    if is_ind:
        title = ["First player", "Score", "Second player", "Campus", "Facility", "Date" ]
        data = [[row[0].capitalize() + " " + row[1].capitalize(), 
                 f"{row[4]} - {row[5]}",
                 row[2].capitalize() + " " + row[3].capitalize(),
                 row[6],
                 row[7],
                 row[8]]  for row in data]

    else:
        title = ["First team", "Score", "Second team", "Campus", "Facility", "Date" ]
        data = [[row[0].title(),
                 f"{row[2]} - {row[3]}",
                 row[1].title(),
                 row[4],
                 row[5],
                 row[6]] for row in data]
        
    return data, title


def manipulate_rank_data(data):
    title = ["Team name", "Captain", "Sport", "Total Score", "Total matches", "Average Score", "Foundation Date"]

    data = [[row[0].title(), # Team name
             row[1], # Team id
             row[2].capitalize() + " " + row[3].capitalize(), # Captain Name
             row[4], # Captain id
             row[5].split(" ")[0], # Sport
             row[6], # Sport id
             row[7], # Total Score
             row[8], # Total Matches
             round(row[9], 1), # Average Score
             row[10]] # Foundation Date
             for row in data] 
    
    return data, title

def manipulate_team_info(data):
    data = data[0]

    team = dict()

    team["name"] = data[0].title()
    team["captain"] = data[1].capitalize() + " " + data[2].capitalize()
    team["sport_type"] = data[3]
    team["sport_id"] = data[4]
    team["fuoundation_date"] = data[5]
    team["team_score"] = data[6]
    team["#_matches"] = data[7]
    team["avrg"] = round(int(data[6]) / int(data[7]), 2)

    return team

def manipulate_facility_info(data):
    facility = dict()

    facility["facility_id"] = data[0]
    facility["name"] = data[1]
    facility["tel_no"] = data[3]
    facility["email"] = data[4]
    facility["address"] = data[5]

    return facility

def manipulate_spor_info(data):
    team = dict()

    return team


    
def manipulate_campus_dropdown():
    cursor = mysql.connection.cursor()
    
    # to get campus names
    cursor.execute("SELECT * FROM campus")  # Adjust the query as needed
    campuses = cursor.fetchall()
    cursor.close()
    
    campus_dropdown = [{"id": campus[0], "name": campus[1]} for campus in campuses]
    print(campus_dropdown)
    return campus_dropdown

    