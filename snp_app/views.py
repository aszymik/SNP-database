from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Species, SNP, Sample, Annotation
from .forms import SNPFilterForm, AnnotationForm

def home(request):
    # Zwraca statystyki bazy danych
    species_count = Species.objects.all().count()
    sample_count = Sample.objects.all().count()
    snp_count = SNP.objects.all().count()

    context = {
        'species_count': species_count,
        'sample_count': sample_count,
        'snp_count': snp_count
    }

    return render(request, 'snp_app/home.html', context)

def snps(request): 
    # Przetwarza informacje strony z SNP
    species_name = request.GET.get('chosen_species')

    if request.method == 'POST':
        form = SNPFilterForm(request.POST)
        annot_form = AnnotationForm(request.POST)
        species_name = request.POST.get('chosen_species')
        region = request.POST.get('region')
        maf_min = request.POST.get('maf_min')
        maf_max = request.POST.get('maf_max')

    else:
        form = SNPFilterForm()
        annot_form = AnnotationForm()
        region = None
        maf_min = None
        maf_max = None

    species = Species.objects.all()
    snps = SNP.objects.all()
    samples = Sample.objects.all()

    # Filtrowanie na podstawie wybranego gatunku
    if species_name:
        chosen_species = Species.objects.get(name=species_name)
        samples = list(samples.filter(species=chosen_species))
        snps = snps.filter(sample__in=samples)

    # Filtrowanie na podstawie regionu
    if region:
        chromosome, start, end = parse_region(region)
        snps = snps.filter(chromosome=chromosome, coordinate__gte=start, coordinate__lte=end)

    # Filtrowanie na podstawie MAF
    if maf_min and maf_max:
        snps = snps.filter(MAF__gte=maf_min, MAF__lte=maf_max)

    # Przekazanie wyników do kontekstu szablonu
    context = {
        'snps': snps,
        'species_name': species_name,
        'species': species, 
        'form' : form,
        'annot_form': annot_form,
    }

    return render(request, 'snp_app/snps.html', context)

def parse_region(region):
    parts = region.split(':')
    chromosome = parts[0][3:]
    start, end = parts[1].split('-')
    return int(chromosome), int(start), int(end)


def annotations(request):
    # Przetwarza formularz dodawania adnotacji i dodaje do bazy danych
    if request.method == 'POST':
        form = AnnotationForm(request.POST)
        if form.is_valid():
            chosen_snp = request.POST.get('chosen_snp')
            snp = SNP.objects.get(pk=chosen_snp)
            type = request.POST.get('type')
            text = request.POST.get('text')
            new_annot = Annotation(type=type,text=text, SNP=snp)
            new_annot.save()
    else:
        form = SNPFilterForm() 

    return redirect(snps)


def save_snp(request):
    # Zapisuje wybrany SNP i zwraca powiązane z nim adnotacje
    annotations = Annotation.objects.all()

    if request.method == 'POST':
        chosen_snp = request.POST.get('chosen_snp')
        snp = SNP.objects.get(pk=chosen_snp)
        annotations = annotations.filter(SNP=snp)

    # Zwracanie wyników w formacie JSON
    data = []
    for annotation in annotations:
         data.append({                    
                'type': annotation.type,
                'text': annotation.text
                })
    return JsonResponse(data, safe=False)
  