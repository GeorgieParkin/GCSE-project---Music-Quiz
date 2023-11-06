import sqlite3
#connect to the database

def LogIn():
    #Login
    db = sqlite3.connect("project database.db")
    c = db.cursor()
    
    
    enteredUsername = input("Username: ")
    enteredPassword = input("Password: ")
    
    
    results = c.execute("SELECT * from userTable WHERE username = ? and password = ?",
                    (enteredUsername,enteredPassword))
    
    results = results.fetchall()
    
    
    if len(results) ==0:
        print("login error")
        return 1, None
    # welcome and instructions
    elif len(results) ==1:
        print("Welcome to The Music Madness Quiz",results[0][0])
        print("""How to play: 
        You will get the name of an artist and the first letter of each word in 
        the title of the song.
        You will then guess the name of the song, 
        Please Use Correct Grammar,
        You will get two chances to get it correct;
        If you get it on the first guess you will get 3 points,
        If you get it on the second guess you will get 1 point,
        If it is incorrect both times they you will be out.""")
        return 0, enteredUsername
        
def randomSong():
    #select a random song
    db = sqlite3.connect("project database.db")
    c = db.cursor()    
    songs = c.execute("SELECT * from songTable")
    songs = songs.fetchall()
    return songs
    
def Question(NoPoints):
    #ask question and input the song
    NoGuesses=0
    correct=0
    songs=randomSong()
    import random
    songnumber = random.randint(0,len(songs)-1)
    print("What is this song?",songs[songnumber][1], songs[songnumber][2])
    Answer = input("Answer: ").lower()
  
    NoGuesses += 1
    
    #check answer and give score
    if Answer == songs[songnumber][0]:
        if NoGuesses == 1:
            print("Well done you scored 3 points!")
            NoPoints+= 3
            correct=1
        elif NoGuesses == 2:
            print("Well done you scored 1 point!")
            NoPoints+=1
            correct=1
    elif Answer != songs[songnumber][0]:
        print("Incorrect")
        if NoGuesses ==1:
            print("Try Again")
            Answer = input("Answer: ").lower()
            NoGuesses += 1
            if Answer == songs[songnumber][0]:
                if NoGuesses == 2:
                    print("Well done you scored 1 points!")
                    NoPoints+= 1
                    correct=1
        elif Answer != songs[songnumber][0]:
            print("Incorrect")
            if NoGuesses ==2:
                print("Well Done")
    return correct, NoPoints

def SaveToDB(enteredUsername):
    #save to database
    db = sqlite3.connect("project database.db")
    c = db.cursor()
    sql = "UPDATE userTable SET currentScore = ? WHERE username = ?"
    c.execute(sql,(NoPoints,enteredUsername))
    db.commit()
    return enteredUsername
    
def ScoreBoard():
    #print top 5 scores
    db = sqlite3.connect("project database.db")
    c = db.cursor()
    sql = c.execute("SELECT username,currentScore FROM userTable ORDER BY currentScore DESC  LIMIT 5")
    results = sql.fetchall()
    for r in results:
        print(r[0].ljust(10,"."),r[1])
    c = db.close()

#calling the code
result=1
correct=1
NoPoints = 0
while result == 1:
    result, enteredUsername = LogIn()
randomSong()
#if answer is correct loop and do again
while correct==1:
    correct, NoPoints = Question(NoPoints)
print("""Bad Luck
Well Done you scored """, NoPoints, " points")
SaveToDB(enteredUsername)
ScoreBoard()