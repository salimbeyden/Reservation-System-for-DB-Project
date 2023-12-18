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