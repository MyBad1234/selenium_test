from django.shortcuts import render

from selenium_client.models import Search


def search_view(request):
    """page for getting """

    if request.method == 'POST':
        company = request.POST.get('company')
        words = request.POST.get('words')

        # delete old searches
        for i in Search.objects.all():
            i.delete()

        # create new objects
        for i in range(100):
            Search.objects.create(
                company=company,
                word=words
            )

    # in process or no
    old_objects = Search.objects.filter(result=None)

    for_input = True
    for_table = False
    if len(old_objects) > 0:
        for_input = False
        for_table = True

    return render(request, 'search.html', context={
        'objects': Search.objects.all(),
        'for_input': for_input,
        'for_table': for_table
    })
