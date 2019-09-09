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
  ]
}

# Initializes values
rentalPrices = {'rentals':[]}
rentalDuration = []
totalPrice = []

# Converts date to a number
def dateConversion(count, chooseDate):
    findDate = drivy['rentals'][count][chooseDate].split('-')
    findDate = [int(x) for x in findDate]
    convertDate = date(findDate[0], findDate[1], findDate[2])
    return convertDate



# Calculates amount due for each car rental
for count in range(len(drivy['rentals'])):

    # Calculates the distance price of the current car rental
    car_id = drivy['rentals'][count]['car_id']
    distancePrice = drivy['cars'][car_id - 1]['price_per_km'] * drivy['rentals'][count]['distance']

    # Calculates the duration of the car rental
    firstDay = dateConversion(count, 'start_date')
    lastDay = dateConversion(count, 'end_date')
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

    # Total price of car rental 
    totalPrice.append(distancePrice + timePrice)

    # Allocates commission due to the people working on the car rental
    rental_id = drivy['rentals'][count]['id']
    rentalPrices['rentals'].append(
        {
            'id': rental_id,
            'price': int(totalPrice[count]),
            'commission': {
                'insurance_fee': int(totalPrice[count] * 0.15),
                'assistance_fee': int(rentalDuration[count] * 100),
                'drivy_fee': int(totalPrice[count] * 0.15 - rentalDuration[count] * 100)
                }
                
            })

# Outputs data 
print(json.dumps(rentalPrices, indent = 3))
