import math
from argparse import ArgumentError, ArgumentParser
import sys
if len(sys.argv) < 5:
    print('Incorrect parameters')

def check_positive(value):
    value = int(value)
    if value <= 0:
        print('Incorrect parameters')
        sys.exit()
    return value

parser = ArgumentParser(description='credit calculator')
parser.add_argument('--type', choices=['annuity', 'diff'],)
parser.add_argument('--interest', type=float)
parser.add_argument('--payment', type=int)
parser.add_argument('--principal', type=float)
parser.add_argument('--periods', type=check_positive)
args = parser.parse_args()



def monthly_interest(annual_interest):
    return annual_interest / (12 * 100)

def diff_payment(p,n, i):
    diff_pay = []
    for m in range(1, n + 1):
        diff_pay.append(math.ceil(p / n + i * (p - (p * (m - 1) / n))))
    return diff_pay

def overpayment(monthly_pay, p):
    return int(sum(monthly_pay) - p)

def periods(a, p, i):
    # periods means number of months to pay
    return math.ceil(math.log(a / (a - i * p), 1 + i))

def credit(a, n, i):
    # credit means credit principal
    # n is periods
    return int(a * (math.pow(1 + i, n) - 1) / (i * math.pow(1 + i, n)))

def annuity(p, n, i):
    # annuity means (annuity) monthly payment
    # n is periods
    return math.ceil(p * i * math.pow(1 + i, n) / (math.pow(1 + i, n) - 1))

if args.type == 'diff':
    p = args.principal
    n = args.periods
    if p is None or n is None or args.interest is None:
        print("Incorrect parameters")
        sys.exit()
    i = monthly_interest(args.interest)

    diff_pay = diff_payment(p, n, i)
    for r in range(n):
        print("Month {}: paid out {}".format(r + 1, diff_pay[r]))
    print()
    print('Overpayment = ' + str(overpayment(diff_pay, p)))

elif args.type == 'annuity':
    if args.periods is None:
        credit = args.principal
        monthly_payment = args.payment
        annual_interest = args.interest
        if credit is None or monthly_payment is None or annual_interest is None:
            print('Incorrect parameters')
            sys.exit()
        i = monthly_interest(annual_interest)
        periods = periods(monthly_payment, credit, i)
        years = int(periods / 12)
        months = periods % 12
        if months == 12:
            months = 0
            years += 1
        output_string = 'You need '
        if years != 0:
            if years == 1:
                output_string += '1 year'
            else:
                output_string += str(years) + ' years'
        if months != 0:
            if months == 1:
                output_string += ' and 1 month'
            else:
                output_string += ' and ' + str(months) + ' months'
        output_string += ' to repay this credit!'
        print(output_string)
        print('Overpayment = ' + str(int(monthly_payment * periods - credit)))

    elif args.principal is None:
        annuity = args.payment
        periods = args.periods
        annual_interest = args.interest
        if annuity is None or periods is None or annual_interest is None:
            print('Incorrect parameters')
            sys.exit()
        i = monthly_interest(annual_interest)
        credit = credit(annuity, periods, i)
        print('Your credit principal = ' + str(credit) + '!')
        print('Overpayment = ' + str(int(annuity * periods - credit)))

    elif args.payment is None:
        credit = args.principal
        periods = args.periods
        annual_interest = args.interest
        if credit is None or periods is None or annual_interest is None:
            print('Incorrect parameters')
            sys.exit()
        i = monthly_interest(annual_interest)
        annuity = annuity(credit, periods, i)
        print('Your annuity payment = ' + str(annuity) + '!')
        print('Overpayment = ' + str(int(annuity * periods - credit)))

