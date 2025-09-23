from django.http import JsonResponse
from django.db.models import Q
from data.models import VisaData, VisaType, Occupation, MonthYear


def get_visa_data(request):
    queryset = VisaData.objects.select_related('month_year', 'visa_type', 'occupation').all()

    # Handle multiple visa types
    visa_types = request.GET.getlist('visa_type')
    if visa_types:
        queryset = queryset.filter(visa_type__name__in=visa_types)

    # Handle multiple occupations
    occupations = request.GET.getlist('occupation')
    if occupations:
        queryset = queryset.filter(occupation__name__in=occupations)

    # Handle multiple EOI statuses
    eoi_statuses = request.GET.getlist('eoi_status')
    if eoi_statuses:
        queryset = queryset.filter(status__in=eoi_statuses)

    # Handle multiple points
    points_list = request.GET.getlist('points')
    if points_list:
        try:
            points_values = [int(p) for p in points_list]
            queryset = queryset.filter(points__in=points_values)
        except ValueError:
            pass

    # Handle month year (single value)
    month_year = request.GET.get('month_year')
    if month_year:
        queryset = queryset.filter(month_year__name__icontains=month_year)

    data = []
    for record in queryset:
        data.append({
            'id': record.id,
            'month_year': record.month_year.name,
            'visa_type': record.visa_type.name,
            'occupation': record.occupation.name,
            'eoi_status': record.status,
            'points': record.points,
            'count_eois': record.count
        })

    return JsonResponse({
        'count': len(data),
        'results': data
    })


def get_filter_options(request):
    visa_types = list(VisaType.objects.values_list('name', flat=True).distinct())
    occupations = list(Occupation.objects.values_list('name', flat=True).distinct())
    month_years = list(MonthYear.objects.values_list('name', flat=True).distinct())
    eoi_statuses = [choice[0] for choice in VisaData.Status.choices]

    points_range = VisaData.objects.values_list('points', flat=True).distinct().order_by('points')
    unique_points = list(points_range)

    return JsonResponse({
        'visa_types': visa_types,
        'occupations': occupations,
        'month_years': month_years,
        'eoi_statuses': eoi_statuses,
        'points': unique_points
    })
