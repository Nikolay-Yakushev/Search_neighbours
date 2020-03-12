from flask import Flask
import psycopg2
import yaml

app = Flask(__name__)

def del_all_pers():
    cur = con.cursor()
    drop_table = 'truncate table users;'
    cur.execute(drop_table)


def del_one_pers(name_srch):
    cur = con.cursor()
    del_pers = f"""delete from users
                  where name=%s;"""
    # according to  psycopg2 documentation
    # following construction is recommended:
    # sql_query = "select name, surname
    #               from table users
    #               where name=%s"
    # cur.execute(sql_query, (params,)).
    # otherwise it wont work correctly,
    # popping up TypeError.
    cur.execute(del_pers, (name_srch,))
    return name_srch


# function insert input parameters into the table
def insert_pers(name, long, lat):
    cur = con.cursor()
    test_ins = """insert into users (id, name, longitude, latitude)
                                            values(default, %s, %s, %s);"""

    cur.execute(test_ins, (name, long, lat,))
    pers_inserted = """select name, longitude, latitude
                        from users
                        where name=%s
                        and latitude=%s
                        and longitude=%s;"""
    # print recently inserted person
    cur.execute(pers_inserted, (name, lat, long,))
    fo = cur.fetchone()
    return fo


# function ST_Distance() - measure distance between selected points
# St_Distance(argv[0] = geolocation of others users
# argv[1]=geolocation of a target)
# function counts distance between target
# and other points, sorting distance in descending order
# (the nearest point is first)
def neighbours(name_srch, radius):
    cur = con.cursor()
    make_point = """update users set 
                            geolocation=ST_MakePoint(longitude, latitude);"""
    # update geolocation column, creating point
    search_neighbours = f"""select name, ST_Distance(u.geolocation, first_user.geolocation) distance
                                    from users u,
                                                lateral(select id, geolocation
                                                        from users 
                                                        where name=%s) as first_user
                                    where u.id != first_user.id
                                    and ST_Distance(u.geolocation, first_user.geolocation)<%s
                                    order by distance;"""
    cur.execute(make_point)
    cur.execute(search_neighbours, (name_srch, radius,))
    fo = cur.fetchall()
    return fo

def is_table():
    pass

# First function that executes.
# Create table if it doesn't exist
# otherwise - fetch all users
def select_all():  # SQL
    cur = con.cursor()
    sel_all = """select to_json(t)
                    from 
                        (select name, longitude, latitude 
                          from users) t;"""

    is_table = """select exists(select * 
                                from information_schema.tables 
                                where table_name=%s);"""
    # Check weather table_name = users exists
    # and show all users
    # if it doesn't, create table users and show all users
    cur.execute(is_table, ('users',))
    if not cur.fetchone()[0]:
        table_create()
        # show all members of a service
        cur.execute(sel_all)
        fl = cur.fetchall()
        return fl
    else:
        cur.execute(sel_all)
        fl = cur.fetchall()
        return fl


# update coordinates of a selected person
def update_coords(name_srch, long, lat):
    # example:
    # input parameter: name_srch=Nick, long=10.5551334, lat=10.910189
    cur = con.cursor()

    sql_select = """select to_json(t)
                    from 
                        (select name, longitude, latitude 
                          from users
                          where name=%s and longitude=%s and latitude=%s) t;"""

    sql_update = f"""update users
                     set longitude=%s,latitude=%s
                     where name=%s;"""
    cur.execute(sql_update, (long, lat, name_srch,))
    cur.execute(sql_select, (name_srch, long, lat,))
    fo = cur.fetchone()
    # output(fo): [name: Nick, longitude: 10.033123, latitude: 10.565789 ]
    return fo


def exten_inst(ext_name):
    cur = con.cursor
    pg_install = """create extension %s;"""
    cur.execute(pg_install, ext_name)


def table_create():
    cur = con.cursor()

    # create table with users of the service
    # geolocation(point:(longitude, latitude), SRID(default 4326))
    # WGS 84 - SRID 4326
    ext_name = 'postgis'
    table_crt = """create table users(
                                        id      	serial,
                                        name    	varchar(10),
                                        longitude 	real,
                                        latitude 	real,
                                        geolocation geography(point, 4326)
                                        );"""

    is_postgis = """select * from pg_extension 
                    where extname=%s;"""
    # if postgis is not installed:
    #   create table and create extension
    # else:
    #   create table only
    cur.execute(is_postgis, (ext_name,))
    if not cur.fetchone()[0]:
        exten_inst(ext_name)
        cur.execute(table_crt)
    else:
        cur.execute(table_crt)


@app.before_first_request
def connect_db():
    with open('config_db.yaml', 'r') as config_db:
        data = yaml.load(config_db, Loader=yaml.FullLoader)
        conn = psycopg2.connect(
            database=data['database'],
            user=data['user'],
            password=data['password'],
            host=data['host'],
            port=data['port'])
        conn.set_session(autocommit=True)
    return conn


con = connect_db()