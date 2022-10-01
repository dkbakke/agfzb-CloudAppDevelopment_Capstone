from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    make_name = models.CharField(null=False,max_length=100)
    make_description = models.CharField(max_length=1000)

    def __str__(self):
        return "Make name: " + self.make_name + "," + \
               "Make description: " + self.make_description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    # Car Model class

    model_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    model_name = models.CharField(
        null=False,
        max_length=100
    )
    dealer_id = models.IntegerField()
    SEDAN = "sedan"
    SUV = "SUV"
    WAGON = "wagon"
    TRUCK = "truck"     
    VEHICLE_TYPE_CHOICES = [
        ( SEDAN,"sedan"),
        (SUV,"SUV"),
        (WAGON,"wagon"),
        (TRUCK,"truck")
    ]
    vehicle_type = models.CharField( 
        null = False,
        max_length = 30, 
        choices = VEHICLE_TYPE_CHOICES,
        default=SEDAN
    )
    model_year = models.DateField()
    

    def __str__(self):
        return "Model name: " + self.model_name + "," + \
            "Model make: " + self.model_make + "," + \
            "Dealer ID: " + self.dealer_id + "," + \
            "Vehicle type: " + self.vehicle_type+ "," + \
            "Model year: " + self.model_year

# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:
# TODO
# maybe missing state

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
# DealerReview class

    def __init__(self, dealer_id, name, purchase, 
        review,purchase_date,car_make, car_model,
        car_year,sentiment,review_id):
        # Dealer id
        self.dealer_id = dealer_id
        # Reviwer Name
        self.name = name
        # Purchase (boolean)
        self.purchase = purchase
        # Review text
        self.review = review
        #Purhcase date
        self.purchase_date = purchase_date
        #Car make
        self.car_make = car_make
        #Car model
        self.car_model = car_model
        #Car year
        self.car_year = car_year
        #Sentiment
        self.sentiment = sentiment
        #Review ID
        self.review_id = review_id

    def __str__(self):
        return "Review by " + self.name +"for "