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


# <HINT> Create a plain Python class `DealerReview` to hold review data
