from .models import Type

def types_processor(request):
    types = Type.objects.all()
    return {'types': types}
