# views.py
import json
from django.http import JsonResponse
from .models import NewsArticle
from datetime import datetime
from django.shortcuts import render,redirect

def import_data(request):
    with open('jsondata.json') as json_file:
        data = json.load(json_file)
    
    


    for item in data:

        added_date = None
        published_date = None

        if item['added']:
            added_date = datetime.strptime(item['added'], '%B, %d %Y %H:%M:%S')

        if item['published']:
            published_date = datetime.strptime(item['published'], '%B, %d %Y %H:%M:%S')


        news_article = NewsArticle(
            end_year=item['end_year'],
            intensity=item['intensity'],
            sector=item['sector'],
            topic=item['topic'],
            insight=item['insight'],
            url=item['url'],
            region=item['region'],
            start_year=item['start_year'],
            impact=item['impact'],
            added=added_date,  # Use the converted date
            published=published_date,
            country=item['country'],
            relevance=item['relevance'],
            pestle=item['pestle'],
            source=item['source'],
            title=item['title'],
            likelihood=item['likelihood']
        )
        news_article.save()

    return JsonResponse({'message': 'Data imported successfully'})


from django.shortcuts import render
from .models import NewsArticle

import json
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import NewsArticle

def view(request):
    # Fetch distinct values for all relevant fields
    regions = NewsArticle.objects.values_list('region', flat=True).distinct()
    end_years = NewsArticle.objects.values_list('end_year', flat=True).distinct()
    topics = NewsArticle.objects.values_list('topic', flat=True).distinct()
    sectors = NewsArticle.objects.values_list('sector', flat=True).distinct()
    pestles = NewsArticle.objects.values_list('pestle', flat=True).distinct()
    sources = NewsArticle.objects.values_list('source', flat=True).distinct()
    countries = NewsArticle.objects.values_list('country', flat=True).distinct()

    # Fetch all NewsArticle objects
    news_articles = NewsArticle.objects.all()

    # Serialize the queryset to JSON
    data = serialize('json', news_articles)

    # Convert JSON string to Python list/dictionary
    json_data = json.loads(data)

    # Pass distinct values and JSON data as context to the template
    context = {
        'regions': list(regions),
        'end_years': list(end_years),
        'topics': list(topics),
        'sectors': list(sectors),
        'pestles': list(pestles),
        'sources': list(sources),
        'countries': list(countries),
        'news_articles': json_data
    }

    # Render the template with the context
    return render(request, 'dashboard.html', context)




from django.http import HttpResponse
from .models import NewsArticle

# def get_all_end_years(request):
#     # Get all end year values, including empty values
#     end_years = NewsArticle.objects.values_list('end_year', flat=True)

#     regions = NewsArticle.objects.values_list('region', flat=True).distinct()

#     # Create a list to store the values
#     end_year_list = []

#     # Loop through the end_years and append them to the list
#     for end_year in end_years:
#         end_year_list.append(end_year)

#     # Print the list of end years
#     print(end_year_list)

#     # Return a response indicating that the data has been printed
#     return HttpResponse("End years have been printed as a list in the terminal.")


# def your_view(request):
#     if request.method == 'POST':
#         selected_item = request.POST.get('selectedDropdownItem')
#         text_field_value = request.POST.get('filterInput')

#         if selected_item == "end_year":

#             try:
                
#                 if int(text_field_value):
                
                 

#                     filter_args = {selected_item: text_field_value}
                
#                     filtered_data = NewsArticle.objects.filter(**filter_args)


#                     result_list = [{'title': article.title, 'intensity': article.intensity, 'likelihood': article.likelihood, 'start_year': article.start_year, 'relevance': article.relevance, 'country': article.country, 'topics': article.topic, 'region': article.region, 'intensity': article.intensity} for article in filtered_data]

#                     print(result_list)
                    
#                     return JsonResponse({'result_list': result_list})
                
#                 else:

#                     return JsonResponse({'error': 'Enter a valid integer value for end_year'})
                
            
#             except:
#                 return JsonResponse({'error': 'Enter a valid integer value for end_year'})

            
#         elif selected_item == "topics":
#             print("")
            



#         print(selected_item , text_field_value)

#         return redirect('view')


from django.core.serializers import serialize
from django.http import JsonResponse
import json

def handle_refresh(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    # Define the fields you want to filter
    filter_fields = ['country', 'region', 'topic', 'end_year', 'sector', 'pestle']

    # Create a dictionary to hold filter conditions
    filter_conditions = {}

    # Build filter conditions dynamically based on the values from the frontend
    for field in filter_fields:
        value = data.get(field)
        if value and value != "":
            filter_conditions[field] = value

    # Use the filter conditions to filter the NewsArticle model
    filtered_articles = NewsArticle.objects.filter(**filter_conditions)

    # Access intensity and likelihood values from the filtered articles
    intensity_values = filtered_articles.values_list('intensity', flat=True)
    likelihood_values = filtered_articles.values_list('likelihood', flat=True)
    year_values = filtered_articles.values_list('start_year', flat=True)
    country_values = filtered_articles.values_list('country', flat=True)
    topic_values = filtered_articles.values_list('topic', flat=True)
    region_values = filtered_articles.values_list('region', flat=True)
    articles_data = filtered_articles.values_list()

    # print(filtered_articles)

    # # Serialize the filtered articles
    # articles_data = json.loads(serialize('json', filtered_articles))

    # Now you can use these values as needed in your backend logic
    # print(f'Intensity Values: {list(intensity_values)}')
    # print(f'Likelihood Values: {list(likelihood_values)}')

    chart = {
        'intensity': list(intensity_values),
        'likelihood': list(likelihood_values),
        'start_year': list(year_values),
        'country': list(country_values),
        'topic': list(topic_values),
        'region': list(region_values),
        'filtered_article':list(articles_data),
    }

    # You can also return a response if needed
    return render(request, 'dashboard.html', chart)
