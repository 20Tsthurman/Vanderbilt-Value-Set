from django.shortcuts import render, get_object_or_404
from .models import ValueSet, Medication
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum

def value_set_list(request):
    # Get the search query from the request's GET parameters
    search_query = request.GET.get('search', '')
    
    if search_query:
        # If a search query is provided, filter the value sets based on the value set name or medication name
        value_sets = ValueSet.objects.filter(
            Q(value_set_name__icontains=search_query) |
            Q(medications__medname__icontains=search_query)
        ).distinct().order_by('value_set_name')  # Add ordering here
    else:
        # If no search query is provided, retrieve all value sets ordered by name
        value_sets = ValueSet.objects.all().order_by('value_set_name')  # Ensure ordering here
    
    # Create a paginator object to split the value sets into pages
    paginator = Paginator(value_sets, 10)  # Show 10 value sets per page
    page = request.GET.get('page')
    
    try:
        # Retrieve the requested page of value sets
        value_sets = paginator.page(page)
    except PageNotAnInteger:
        # If the page number is not an integer, return the first page
        value_sets = paginator.page(1)
    except EmptyPage:
        # If the page number is out of range, return the last page
        value_sets = paginator.page(paginator.num_pages)
    
    # Render the value set list template with the value sets, search query, and pagination object
    return render(request, 'valuesets/value_set_list.html', {
        'value_sets': value_sets,
        'search_query': search_query,
        'page_obj': value_sets
    })

def value_set_detail(request, value_set_id):
    # Retrieve the value set with the specified ID or return a 404 error if not found
    value_set = get_object_or_404(ValueSet, value_set_id=value_set_id)
    
    # Render the value set detail template with the value set object
    return render(request, 'valuesets/value_set_detail.html', {'value_set': value_set})

def value_set_comparison(request):
    # Retrieve all value sets ordered by name
    value_sets = ValueSet.objects.all().order_by('value_set_name')
    
    # Get the selected value set IDs from the request's GET parameters
    selected_value_set_ids = request.GET.getlist('value_set_ids')
    
    # Retrieve the selected value sets based on the IDs
    selected_value_sets = ValueSet.objects.filter(value_set_id__in=selected_value_set_ids)
    
    # Find common medications among the selected value sets
    common_medications = Medication.objects.none()
    if selected_value_sets:
        common_medications = selected_value_sets[0].medications.all()
        for value_set in selected_value_sets[1:]:
            common_medications = common_medications & value_set.medications.all()
    
    # Calculate the total number of patients across all medications
    total_patients = Medication.objects.aggregate(total_patients=Sum('patients'))['total_patients']
    
    # Calculate the percentage of patients taking medications in each selected value set
    for value_set in selected_value_sets:
        value_set.total_patients_percentage = (
            value_set.medications.aggregate(value_set_patients=Sum('patients'))['value_set_patients']
            / total_patients * 100
        ) if total_patients else 0
    
    # Calculate the column span for the common medications row in the comparison table
    column_span = len(selected_value_sets) + 1
    
    # Render the value set comparison template with the necessary data
    return render(request, 'valuesets/value_set_comparison.html', {
        'value_sets': value_sets,
        'selected_value_sets': selected_value_sets,
        'common_medications': common_medications,
        'column_span': column_span,
    })