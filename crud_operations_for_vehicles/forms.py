from django import forms
from vehicles.models import Vehicle


class CreateVehicleForm(forms.ModelForm):
    vehicle_model = forms.CharField(label='Model', max_length=100, required=True)
    vehicle_brand = forms.CharField(label='Brand', max_length=100, required=True)
    vehicle_type = forms.ChoiceField(label='Type', choices=Vehicle.TYPE_CHOICES, required=True)
    vehicle_price = forms.FloatField(label='Price', required=True)
    vehicle_status = forms.ChoiceField(label='Status', choices = Vehicle.STATUS_CHOICES ,required=True)  
    vehicle_image = forms.ImageField(label='Image', required=True)

    class Meta:
        model = Vehicle
        fields = ['vehicle_model', 'vehicle_brand', 'vehicle_type', 'vehicle_price', 'vehicle_status' , 'vehicle_image']

    def save(self, commit=True):
        vehicle = super().save(commit=False)
        # Check if the vehicle object is being created properly
        print("Vehicle created:", vehicle)
        image = self.cleaned_data.get('vehicle_image')
        if image:
            image_binary =  image.read()
            vehicle.vehicle_blobimage = image_binary
        if commit:
            print("Commiting")
            vehicle.save()
            
        return vehicle

# class CreateVehicleForm(forms.ModelForm):
#     # model = forms.CharField(label='Model', max_length=100, required=True)
#     # brand = forms.CharField(label='Brand', max_length=100, required=True)
#     # vehicle_type = forms.ChoiceField(label='Type', required=True)
#     # vehicle_price = forms.FloatField(label='Price', required=True)
#     # vehicle_status = forms.ChoiceField(label='Status', required=True)
#     # vehicle_blobimage = forms.ImageField(label='Image', required=True)

#     class Meta:
#         model = Vehicle
#         fields = ['vehicle_model', 'vehicle_brand', 'vehicle_type', 'vehicle_price', 'vehicle_status']#, 'vehicle_blobimage']
    
#     # vehicle_blobimage = forms.ImageField(label='Image', required=True)

#     def save(self, commit=True):
#        # Clean and validate the data first
#        vehicle = super().save(commit=False)  # Get the form data without committing to the DB yet
#     #    image = self.cleaned_data.get('vehicle_blobimage')  # Get the image file
       
#     #    if image:
#     #        vehicle.vehicle_blobimage = image.read()  # Convert image to binary data

#        if commit:
#            vehicle.save()  # Save the Vehicle instance to the DB
#        return vehicle
#     #    if self.is_valid():
#     #        # Process the image (convert to binary)
#     #        image = self.cleaned_data['vehicle_blobimage']
#     #        image_binary = image.read()  # Read image as binary data

#     #        # Create a new Vehicle object and save it
#     #        vehicle = Vehicle(
#     #            model=self.cleaned_data['model'],
#     #            brand=self.cleaned_data['brand'],
#     #            vehicle_type=self.cleaned_data['vehicle_type'],
#     #            vehicle_price=self.cleaned_data['vehicle_price'],
#     #            vehicle_status=self.cleaned_data['vehicle_status'],
#     #            vehicle_blobimage=image_binary  # Save the binary data
#     #        )
#     #        vehicle.save()
#     #        return vehicle  # Optionally return the saved vehicle object
