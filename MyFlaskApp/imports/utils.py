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
