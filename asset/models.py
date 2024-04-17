from django.db import models

class Asset(models.Model):
    AssetName = models.CharField(max_length=255)
    Category = models.CharField(max_length=100)
    Department = models.CharField(max_length=100)
    Office = models.CharField(max_length=100, null=True)
    Location = models.CharField(max_length=100, null=True)
    Status = models.CharField(max_length=100, null=True)
    PurchaseDate = models.DateField( null=True)
    PurchasePrice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Depreciation = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    WarrantyExpirationDate = models.DateField( null=True)
    AssignedTo = models.CharField(max_length=100, null=True)
    LastMaintenanceDate = models.DateField(null=True)
    NextMaintenanceDate = models.DateField(null=True)
    Supplier_id = models.IntegerField( null=True)  # Assuming foreign key will be handled later
    SerialNumber = models.CharField(max_length=100,  null=True)
    Model = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.AssetName
