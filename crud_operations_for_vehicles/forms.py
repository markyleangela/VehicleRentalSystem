from django import forms
from vehicles.models import Vehicle

class CreateVehicleForm(forms.ModelForm):
    vehicle_model = forms.CharField(label='Model', max_length=100, required=True)
    vehicle_brand = forms.CharField(label='Brand', max_length=100, required=True)
    vehicle_type = forms.ChoiceField(
        label='Vehicle Type',
        choices=[('', 'Select')] + Vehicle.TYPE_CHOICES,  # Default empty choice
        required=True
    )
    vehicle_price = forms.FloatField(label='Price/Day', required=True)
    vehicle_status = forms.ChoiceField(
        label='Status',
        choices=[('', 'Select')] + Vehicle.STATUS_CHOICES,  # Default empty choice
        required=True  
    )
    vehicle_description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'rows': 4}),
        required=True
    )
    vehicle_transmission = forms.ChoiceField(
        label='Transmission',
        choices=[('', 'Select')] + Vehicle.TRANSMISSION_CHOICES,  # Default empty choice
        required=True   
    )
    vehicle_cargo = forms.ChoiceField(
        label='Cargo Capacity',
        choices=[('', 'Select')] + Vehicle.CARGO_CHOICES,  # Default empty choice
        required=True   
    )
    vehicle_fuel = forms.ChoiceField(
        label='Fuel Type',
        choices=[('', 'Select')] + Vehicle.FUEL_CHOICES,  # Default empty choice
        required=True   
    )
    vehicle_image = forms.ImageField(label = '',required=False) 
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_model', 'vehicle_brand', 'vehicle_type', 'vehicle_price',
            'vehicle_status', 'vehicle_description', 'vehicle_transmission',
            'vehicle_cargo', 'vehicle_fuel'
        ]

    def save(self, commit=True):
        # commit=False to process additional fields (image) before saving
        vehicle = super().save(commit=False)
        image = self.cleaned_data.get('vehicle_image')
        if image:
            vehicle.vehicle_blobimage = image.read()  # Save image as binary
        if commit:
            vehicle.save()
        return vehicle
