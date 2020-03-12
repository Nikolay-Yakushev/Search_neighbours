from time import time
import flask_request
from matplotlib import pyplot as plt


# decorator to measure functions' time execution
def time_dec(original_func):
    def wrapper(*args):
        start = time()
        counter = original_func(*args)  # return number of times function was executed
        end = time()
        dif = end - start
        # function name, payload(10, 100, 1000...), time of execution
        # example: ('del_one_pers', 10): 0.029580116271972656
        exec_time[original_func.__name__, gen, counter] = dif

    return wrapper


exec_time = {}


def person_gen(pers_range):
    for pers in range(0, pers_range):
        flask_request.post_pers(pers)


@time_dec
def upd_coords(pers_range):
    for pers in range(0, pers_range):
        flask_request.put_upd(pers)
    return pers_range


@time_dec
def neighbour(pers_range):
    for pers in range(0, pers_range):
        res = flask_request.pers_near(pers)
        # print(res)
    return pers_range


@time_dec
def del_one_pers(pers_range):
    # DELETE METHODS :
    # delete_all_mhd()     1) DELETE WHOLE TABLE
    # delete_one_mhd(0, pers_range) 2) DELETE USERS IN TABLE ONE BY ONE
    for pers in range(0, pers_range):
        flask_request.delete_one_mhd(pers)
    return pers_range


# truncate table users, just to mane sure every person is deleted
def del_all():
    flask_request.delete_all_mhd()


def build_graph():
    with open('.gitignore/tests_results.txt', 'w') as test_results:
        dots = {}
        dots_axis = dots.fromkeys(persons_range, 0)
        for key, value in exec_time.items():
            dots_axis[key[1]] += value
            # example : key=('neighbour', 1000, 5): time_avg=0.008932065963745118
            # key = function that executed='neighbour', number of users in users BD=1000,
            # how many time func was executed=5]
            # value =
        for key, value in exec_time.items():
            dots_axis[key[1]] = dots_axis[key[1]] / key[2]
            # test_results.write(f'{key=}: time_avg={value / key[2]}')
            test_results.write(f'{key=}: time_avg={dots_axis[key[1]] / key[2]}')
            test_results.write('\n')

    lists_persons = dots_axis.items()

    plt.xlabel('seconds')
    plt.ylabel('persons')
    plt.title(f'Payload table')

    axis_x, axis_y = zip(*lists_persons)
    plt.plot(axis_y, axis_x)
    plt.savefig('graph.png')


# check time of functions execution with payload of 10, 100, 1000... users

def generate_pers(pers_range, avg=5):
    flask_request.select_all()
    person_gen(pers_range)
    upd_coords(avg)
    neighbour(avg)
    del_one_pers(avg)
    del_all()


# testing
persons_range = [10, 15, 100, 1000, 5000, 10000, 50000, 100000]
for gen in persons_range:
    generate_pers(gen)

build_graph()
