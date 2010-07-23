from applications.collection.models import letters as ls

def letters(request):
    return {
        'letters': ls,
    }
