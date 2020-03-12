import requests
from random import uniform, randint

def get_pers():  # reference: select_all persons
    r = requests.get('http://localhost:5000/persons')
    return r.json()


def post_pers(user):  # reference: person_gen
    payload = {'name': f'{user}',
               'longitude': f'{uniform(10.000, 10.999)}',
               'latitude': f'{uniform(10.000, 10.999)}'}
    r = requests.post('http://localhost:5000/person', params=payload)


def put_upd(person):  # reference: update_coords
    payload = {'name': f"{person}",
               'longitude': f'{uniform(10.000, 10.999)}',
               'latitude': f'{uniform(10.000, 10.999)}'}
    r = requests.put('http://localhost:5000/person', params=payload)


def delete_all_mhd():  # reference: del_all_pers
    r = requests.delete('http://localhost:5000/persons')


def delete_one_mhd(person):  # reference: del_one_pers
    payload = {'name': f"{person}"}
    r = requests.delete('http://localhost:5000/person', params=payload)


def pers_near(person):  # reference: neighbours
    payload = {'name': f"{person}",
               'distance': f'{randint(1000, 10000)}'}
    r = requests.get('http://localhost:5000/persons_near', params=payload)
    return r.content.decode() # todo разобраться с представлением json?

# @time_dec
def select_all():
    get_pers()
