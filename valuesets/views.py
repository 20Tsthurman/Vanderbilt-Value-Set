from django.shortcuts import render, get_object_or_404
from .models import ValueSet, Medication
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum

def value_set_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        value_sets = ValueSet.objects.filter(
            Q(value_set_name__icontains=search_query) |
            Q(medications__medname__icontains=search_query)
        ).distinct()
    else:
        value_sets = ValueSet.objects.all().order_by('value_set_name')

    paginator = Paginator(value_sets, 10)  # Show 10 value sets per page
    page = request.GET.get('page')
    try:
        value_sets = paginator.page(page)
    except PageNotAnInteger:
        value_sets = paginator.page(1)
    except EmptyPage:
        value_sets = paginator.page(paginator.num_pages)

    return render(request, 'valuesets/value_set_list.html', {'value_sets': value_sets, 'search_query': search_query, 'page_obj': value_sets})

def value_set_detail(request, value_set_id):
    value_set = get_object_or_404(ValueSet, value_set_id=value_set_id)
    return render(request, 'valuesets/value_set_detail.html', {'value_set': value_set})

def value_set_comparison(request):
    value_sets = ValueSet.objects.all().order_by('value_set_name')
    selected_value_set_ids = request.GET.getlist('value_set_ids')
    selected_value_sets = ValueSet.objects.filter(value_set_id__in=selected_value_set_ids)

    # Find common medications
    common_medications = Medication.objects.none()
    if selected_value_sets:
        common_medications = selected_value_sets[0].medications.all()
        for value_set in selected_value_sets[1:]:
            common_medications = common_medications & value_set.medications.all()

    # Calculate the percentage of patients taking medications in each value set
    total_patients = Medication.objects.aggregate(total_patients=Sum('patients'))['total_patients']
    for value_set in selected_value_sets:
        value_set.total_patients_percentage = value_set.medications.aggregate(
            value_set_patients=Sum('patients')
        )['value_set_patients'] / total_patients * 100 if total_patients else 0

    # Calculate column span for common medications row
    column_span = len(selected_value_sets) + 1

    return render(request, 'valuesets/value_set_comparison.html', {
        'value_sets': value_sets,
        'selected_value_sets': selected_value_sets,
        'common_medications': common_medications,
        'column_span': column_span,
    })
