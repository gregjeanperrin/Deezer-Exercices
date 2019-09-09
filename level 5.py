from datetime import date
import json

# Input data
drivy = {
  "cars": [
    { "id": 1, "price_per_day": 2000, "price_per_km": 10 }
  ],
  "rentals": [
    { "id": 1, "car_id": 1, "start_date": "2015-12-8", "end_date": "2015-12-8", "distance": 100 },
    { "id": 2, "car_id": 1, "start_date": "2015-03-31", "end_date": "2015-04-01", "distance": 300 },
    { "id": 3, "car_id": 1, "start_date": "2015-07-3", "end_date": "2015-07-14", "distance": 1000 }
  ],
  "options": [
    { "id": 1, "rental_id": 1, "type": "gps" },
    { "id": 2, "rental_id": 1, "type": "baby_seat" },
    { "id": 3, "rental_id": 2, "type": "additional_insurance" }
  ]
}

# Initializes values
rentalPrices = {'rentals':[]}
rentalDuration = []
totalPrice = []
optionPrices = [[] for x in range(len(drivy['rentals']))]




# Removes duplicate options in the same car rental
def delRepetitiveOptions(count):
    optionPrices[count] = set(optionPrices[count])
    optionPrices[count] = list(optionPrices[count])


def checkErrors(count):
    global error, warning
    
    # Checks the car_id is valid
    if len(drivy['cars']) < drivy['rentals'][count]['car_id']:
        warning = 'car id does not exist'
        error = True

    # Checks the distance entered is an integer
    elif type(drivy['rentals'][count]['distance']) != int:
        warning = 'distance is not an integer'
        error = True

# If date is valid, it is converted to a number
def dateConversion(count, chooseDate):
    global error, warning
    year, month, day = drivy['rentals'][count][chooseDate].split('-')
    try:
        convertDate = date(int(year), int(month), int(day))
        return convertDate
    except:
        warning = chooseDate + ' invalid'
        error = True

# Computes the current car rental's additional prices due to its options     
def addedPrices(option, price, person, count):
    if option in rentalPrices['rentals'][count]['options']:
        individualPrice['driver'] += price * rentalDuration[count]
        individualPrice[person] += price * rentalDuration[count]




# Allocates each option to its attributed car rental 
for count in range(len(drivy['options'])):
    rental_id = drivy['options'][count]['rental_id']
    optionType = drivy['options'][count]['type']
    optionPrices[rental_id - 1].append(optionType)


# Calculates amount due for each car rental
for count in range(len(drivy['rentals'])):
    
    # Checks for potential errors
    error = False
    delRepetitiveOptions(count)
    checkErrors(count)

    firstDay = dateConversion(count, 'start_date')
    lastDay = dateConversion(count, 'end_date')

    if error:
        rentalDuration.append(0)
        totalPrice.append(0)
        rentalPrices['rentals'].append({'id': count + 1, 'error': warning})
        continue

    # Calculates the distance price of the current car rental
    car_id = drivy['rentals'][count]['car_id']
    distancePrice = drivy['cars'][car_id - 1]['price_per_km'] * drivy['rentals'][count]['distance']

    # Calculates the duration of the car rental
    rentalDuration.append((lastDay - firstDay).days + 1)

    # Calculates the time price of the current car rental
    timePrice = 0
    for days in range(rentalDuration[count]):
        if days < 1:
            timePrice += 2000
        elif (1 <= days < 4):
            timePrice += (2000 * 0.9)
        elif (4 <= days < 10):
            timePrice += (2000 * 0.7)
        else:
            timePrice += (2000 * 0.5)

    # Total price of car rental without options taken into account
    totalPrice.append(distancePrice + timePrice)

    rental_id = drivy['rentals'][count]['id']
    rentalPrices['rentals'].append({'id': rental_id, 'options': optionPrices[count], 'actions': []})

    # Depending on the person it llocates amount (due to them) or (to be paid by them)
    individualPrice = {'driver': totalPrice[count],
                        'owner': totalPrice[count] * 0.7,
                        'insurance': totalPrice[count] * 0.15,
                        'assistance': rentalDuration[count] * 100,
                        'drivy': totalPrice[count] * 0.15 - rentalDuration[count] * 100}

    # People involved in the car rental
    people = individualPrice.keys()

    # Additional prices taken into account
    addedPrices('gps', 500, 'owner', count)
    addedPrices('baby_seat', 200, 'owner', count)
    addedPrices('additional_insurance', 1000, 'drivy', count)

    # Depending on the person it attributes (their amount owed and how to pay them)
    # or (their amount due and how they should pay)
    for person in people:
        rentalPrices['rentals'][count]['actions'].append({'who': person,
                                                          'type': 'credit',
                                                          'amount': int(individualPrice[person])})
        if person == 'driver':
            index = person.index('driver')
            rentalPrices['rentals'][count]['actions'][index]['type'] = 'debit'


# Outputs data           
print(json.dumps(rentalPrices, indent = 3))

