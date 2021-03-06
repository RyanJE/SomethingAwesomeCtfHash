import os
import sqlite3
from encoding import caesar
import string
import random
import secrets

os.environ["FLASK_APP"] = "app.py"


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def generateFlag(n):
    random.seed(n)
    return "FLAG"+randomString(20)



#DONT LOOK AT THIS FUNCTION YOU CHEATER, IT'LL RUIN EVERYTHING (unless you are on part 2, in which case its fair game)
def startup(level1Pass, level2Pass, level3Pass):
    conn = sqlite3.connect('./templates/level1/data.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (username text, secret text)")
    for (user, secret) in level1UserList(level1Pass):
        c.execute("INSERT INTO users VALUES ('{}','{}')".format(user, secret))
    conn.commit()
    conn.close()
    
    conn = sqlite3.connect('./templates/level2/data.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (username text, password text)")
    c.execute("DROP TABLE IF EXISTS posts")
    c.execute("CREATE TABLE posts (user text, post text)")
    for (user, password) in level2UserList():
        c.execute("INSERT INTO users VALUES ('{}','{}')".format(user, password))
    conn.commit()
    conn.close()
    f = open('./templates/level2/secretlvl2password.txt', "w")
    f.write(level2Pass)
    f.close()

    conn = sqlite3.connect('./templates/level3/data.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (username text, password text)")
    for (user, password) in [("Hackerman435", randomString(100))]:
        c.execute("INSERT INTO users VALUES ('{}','{}')".format(user, password))
    conn.commit()
    conn.close()




def level1UserList(level1Pass):
    alphabets = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
    return [("admin",caesar("SecretIsInUser554", len("SecretIsInUser554"), alphabets)), 
    ("User554",caesar(level1Pass, len(level1Pass), alphabets)), 
    ("User6000",caesar("NotThisOne", len("NotThisOne"), alphabets)), ("User666",caesar("ThisOneNotHere", len("ThisOneNotHere"), alphabets)),
    ("User555",caesar("abcdefghijklmnopqrstuvwxyz", len("abcdefghijklmnopqrstuvwxyz"), alphabets))]

def level2UserList():
    return [("admin", randomString(100))] + [(i, randomString(100)) for i in string.ascii_letters]


if __name__ == "__main__":
    l1Seed = secrets.randbelow(50000)
    l2Seed = secrets.randbelow(50000)
    l3Seed = secrets.randbelow(50000)
    os.environ["l1Seed"] = str(l1Seed)
    os.environ["l2Seed"] = str(l2Seed)
    os.environ["l3Seed"] = str(l3Seed)
    startup(generateFlag(l1Seed), generateFlag(l2Seed), generateFlag(l3Seed))
    os.system("flask run")