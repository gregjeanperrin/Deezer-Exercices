from datetime import date
import json

# Input data
drivy = {
  "cars": [
    { "id": 1, "price_per_day": 2000, "price_per_km": 10 },
    { "id": 2, "price_per_day": 3000, "price_per_km": 15 },
    { "id": 3, "price_per_day": 1700, "price_per_km": 8 }
  ],
  "rentals": [
    { "id": 1, "car_id": 1, "start_date": "2017-12-8", "end_date": "2017-12-10", "distance": 100 },
    { "id": 2, "car_id": 1, "start_date": "2017-12-14", "end_date": "2017-12-18", "distance": 550 },
    { "id": 3, "car_id": 2, "start_date": "2017-12-8", "end_date": "2017-12-10", "distance": 150 }
  ]
}

# Initializes values
rentalPrices = {'rentals':[]}
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
    rentalDuration = (lastDay - firstDay).days + 1

    # Calculates the time price of the current car rental
    timePrice = drivy['cars'][car_id - 1]['price_per_day'] * rentalDuration

    # Total price of car rental
    totalPrice.append(distancePrice + timePrice)

    # Computes amount due by the driver for each car rental
    rental_id = drivy['rentals'][count]['id']
    rentalPrices['rentals'].append({'id': rental_id, 'price': totalPrice[count]})


# Outputs data 
print(json.dumps(rentalPrices, indent = 3))


