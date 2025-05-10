import random

def uncertain(number:float, lower: float, upper: float):
    '''
    get a random number around a given number within a preferred lower bound and upper bound
    :param number: given number
    :param lower: a float in [0,1] defining how much the lower bound is lower than the given number, e.g. lower = 0.3 means the lower bound is 0.7*number
    :param upper: a float in [0,1] defining how much the upper bound is higher than the given number, e.g. upper = 0.3 means the lower bound is 1.3*number
    :return: a random number in the range [lowerbound, upperbound]
    '''
    lowerbound = number*(1-lower)
    upperbound = number*(1+upper)
    uncertainNum = random.triangular(lowerbound, upperbound)

    return uncertainNum


'''if __name__ == '__main__':
    print(uncertain(1.233, 0.1, 0.1))'''