print('Interest Calculator:')

def calcInterest(amount, roi, yrs):
    total = (amount * pow(1 + (roi/100), yrs))
    interest = total - amount

    return interest

amount = float(input('Principal amount ?'))
roi = float(input('Rate of Interest ?'))
yrs = int(input('Duration (no. of years) ?'))

print('\nInterest = %0.2f' %calcInterest(amount,roi,yrs))