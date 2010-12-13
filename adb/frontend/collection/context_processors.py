from adb.frontend.collection.models import letters as ls

def letters(request):
    return {
        'letters': ls,
    }
