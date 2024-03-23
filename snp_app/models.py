from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# species – sample: jeden do wielu
# species – SNP: jeden do wielu
# sample – SNP: wiele do wielu (dwa osobniki mogą mieć ten sam snip)

class Animal(models.Model):
    name = models.CharField(max_length=200)
    species = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)

class Species(models.Model):
    name = models.CharField(max_length=200)
    #image_src = models.CharField(max_length=200)  # ścieżka do zdjęcia (w folderze static)
    image = models.ImageField(upload_to='images/')
    reference_genome = models.CharField(max_length=200, unique=True, null=False)

class Sample(models.Model):
    name = models.CharField(max_length=200)
    sampling_date = models.DateField()
    sequencing_date = models.DateField()
    specimen = models.CharField(max_length=100)  # nazwa osobnika
    tissue = models.CharField(max_length=100)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    # SNP = models.ForeignKey(Snip, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sampling_date', 'specimen', 'species', 'tissue',)
        constraints = [
            models.CheckConstraint(check=models.Q(sequencing_date__gte=models.F('sampling_date')),
                name='sequencing_later_than_sampling')
        ]

class SNP(models.Model):
    chromosome = models.IntegerField()
    coordinate = models.IntegerField()  # pozycja w genomie referencyjnym
    reference_allele = models.CharField(max_length=1)  # nukleotyd w genomie referencyjnym
    alternative_allele = models.CharField(max_length=1)
    MAF = models.FloatField()
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

    class Meta:
        # jeden SNP dla danego chromosomu i koordynatu 
        unique_together = ('chromosome', 'coordinate',)
        
        constraints = [
            # reference allele musi byc różny od alternative allele
            models.CheckConstraint(check=~models.Q(alternative_allele = models.F('reference_allele')),
                name='snips_cannot_be_equal'),
            # MAF między 0 a 1    
            models.CheckConstraint(check=models.Q(MAF__gte=0.0) & models.Q(MAF__lte=1.0),
                name='MAF_range')
        ]

class Annotation(models.Model):
    text = models.CharField(max_length=5000)
    type = models.CharField(max_length=200)
    SNP = models.ForeignKey(SNP, on_delete=models.CASCADE)
