from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from .models import Client
from rest_framework import viewsets, permissions
from .serializers import ClientSerializer
from .permissions import IsManagerUser

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsManagerUser]  # Define this permission class
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
def client_list_view(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def clients_view(request):
    return render(request, 'client_list.html')


def is_admin(user):
    return user.is_authenticated and user.is_admin

# Helper function to check if the user is a manager
def is_manager(user):
    return user.is_authenticated and user.is_manager

@require_http_methods(["GET"])
def client_list(request):
    # Only authenticated users can view the list
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    
    # Retrieve all clients and serialize the data
    clients = Client.objects.all().values('id', 'org_name', 'project_name', 'description', 'estimation')
    return JsonResponse(list(clients), safe=False)

@require_http_methods(["GET", "DELETE", "PUT"])
def client_detail(request, client_id):
    # Try to get the client by ID, return 404 if not found
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        raise Http404("Client does not exist")
    
    if request.method == 'GET':
        # Serialize client data
        return JsonResponse({'id': client.id, 'org_name': client.org_name, 'project_name': client.project_name, 'description': client.description, 'estimation': client.estimation})

    elif request.method == 'DELETE':
        # Only admins can delete a client
        if not is_admin(request.user):
            return HttpResponse(status=403)
        client.delete()
        return HttpResponse(status=204)

    elif request.method == 'PUT':
        # Only managers can update a client
        if not is_manager(request.user):
            return HttpResponse(status=403)
# to be implemented
        return JsonResponse({'id': client.id, 'org_name': client.org_name, 'project_name': client.project_name, 'description': client.description, 'estimation': client.estimation})
    
def actions(request):
    return render(request, 'action.html')