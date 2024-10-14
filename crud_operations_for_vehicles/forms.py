from django import forms
from vehicles.models import Vehicle


class CreateVehicleForm(forms.ModelForm):
    vehicle_model = forms.CharField(label='Model', max_length=100, required=True)
    vehicle_brand = forms.CharField(label='Brand', max_length=100, required=True)
    vehicle_type = forms.ChoiceField(label='Type', choices=Vehicle.TYPE_CHOICES, required=True)
    vehicle_price = forms.FloatField(label='Price', required=True)
    vehicle_status = forms.ChoiceField(label='Status', choices = Vehicle.STATUS_CHOICES ,required=True)  
    vehicle_image = forms.ImageField(label='Image', required=False)

    class Meta:
        model = Vehicle
        fields = ['vehicle_model', 'vehicle_brand', 'vehicle_type', 'vehicle_price', 'vehicle_status' , 'vehicle_image']

    def save(self, commit=True):
        vehicle = super().save(commit=False)
        print("Vehicle created:", vehicle)
        image = self.cleaned_data.get('vehicle_image')
        if image:
            image_binary =  image.read()
            vehicle.vehicle_blobimage = image_binary
        if commit:
            print("Commiting")
            vehicle.save()
            
        return vehicle

