import sqlite3
import os
    
def select_movies(list_names, max_length):
    """
    (list, int) --> list
    
    returns a list of randomly id's of movies in the database that don't exceed the maximum length given (optional).
    The size of this returned list is one more than the amount of spectators.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "movie_db.sqlite") 

    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    
    size=len(list_names)+1
    list_movies=[]
    length_db = cur.execute('SELECT COUNT(*) FROM movie')
        #when no maximum length is given
    if max_length==None:
        if size <= length_db:
            cur.execute('SELECT m_id FROM movie ORDER BY RANDOM() LIMIT(?)',(size, ))
            for mov in cur:
                list_movies.append(mov)
        else:
            print("There are not enough movies found.\nPlease cluster viewers in groups")
            conn.close()
            exit()
    #selecting based on the maximum length
    else:
        try: 
            cur.execute('SELECT m_id FROM movie WHERE length<=? ORDER BY RANDOM() LIMIT(?)',(max_length, size))
            for mov in cur:
                list_movies.append(mov)         
        except:
            print("There are not enough movies found with your given criteria.\nPlease cluster viewers in groups or give a higher maximum duration.")
            conn.close()
            exit()
    conn.close() 
    return list_movies
    

def movie_info_selection(list_movies):
    """
    (list of tuples) --> none
    
    Prints out the interesting information about the selected movies from the database.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "movie_db.sqlite") 

    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    
    count=1
    for movie in list_movies:
        
        cur.execute('SELECT title FROM movie WHERE m_id==?',(movie[0],))
        title=cur.fetchone()
        
        cur.execute('SELECT info FROM movie WHERE m_id==?',(movie[0],))
        info=cur.fetchone()
        
        cur.execute('SELECT year FROM year WHERE y_id IN(SELECT y_id FROM movie WHERE m_id==?)',(movie[0],))
        year=cur.fetchone()
        
        cur.execute('SELECT name_genre FROM genre WHERE g_id IN(SELECT g_id FROM defined_as WHERE m_id==?)',(movie[0],))
        rows=cur.fetchall()
        genres=''
        for genre in rows:
            #first name without comma
            if len(genres)==0:
                genres+=genre[0]
            else:
                genres+=", "+genre[0]
            
        cur.execute('SELECT name_director FROM director WHERE d_id IN(SELECT d_id FROM directed_by WHERE m_id==?)',(movie[0],))
        rows=cur.fetchall() 
        directors=''
        for director in rows:
            if len(directors)==0:
                directors+=director[0]
            else:
                directors+=", "+director[0]
            
        cur.execute('SELECT name_country FROM country WHERE c_id IN(SELECT c_id FROM produced_in WHERE m_id==?)',(movie[0],))
        rows=cur.fetchall()
        countries=''
        for country in rows:
            if len(countries)==0:
                countries+=country[0]
            else:
                countries+=", "+country[0]
        
        print("--> Proposal {0}:\n\n\t{1}\n\n{2}\n\n{3}\n\ndirector(s): {4}\n\n{5}\t{6}\n\n".format(count, title[0].upper(), info[0], genres, directors, countries, year[0]))
        count+=1

    conn.close()
    
        
# SELECT * FROM table WHERE id IN (SELECT id FROM table ORDER BY RANDOM() LIMIT x)
    

