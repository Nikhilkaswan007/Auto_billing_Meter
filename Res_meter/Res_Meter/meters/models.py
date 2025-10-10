from django.db import models
from django.utils import timezone

class Meter(models.Model):
    # Unique device ID from the physical meter
    device_id = models.CharField(max_length=100, unique=True)
    
    # Basic Info
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    # Location & Contact Information
    location = models.CharField(max_length=300, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.device_id})"
    

class MeterSpecification(models.Model):
    meter = models.OneToOneField(Meter, on_delete=models.CASCADE, related_name='specification')
    
    # Technical Specifications (free text - type whatever you want)
    capacity = models.CharField(max_length=100, blank=True)
    voltage = models.CharField(max_length=100, blank=True)
    ampere = models.CharField(max_length=100, blank=True)
    additional_specs = models.TextField(blank=True)
    
    # Limits for automatic cutoff
    voltage_upper_limit = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    voltage_lower_limit = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ampere_upper_limit = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ampere_lower_limit = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Specs for {self.meter.name}"
    
class MeterReading(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name='readings')
    
    # Energy consumption data
    kilowatt_hours = models.DecimalField(max_digits=10, decimal_places=3)
    
    # Current voltage and ampere at time of reading
    current_voltage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    current_ampere = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # When this reading was recorded
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']  # Newest readings first
    
    def __str__(self):
        return f"{self.meter.name} - {self.kilowatt_hours} kWh at {self.timestamp}"