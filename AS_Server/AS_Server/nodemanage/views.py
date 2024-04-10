from django.http import JsonResponse
from .models import NodeTable
import datetime, json


# Create your views here.
def node_update(request, pk):
    if request.method == "POST":
        try:
            json_data = request.POST.get("update_form")
            json_data = json.loads(json_data)
            update_instance = NodeTable.objects.get(node_id=pk)
            for key, value in json_data.items():
                setattr(update_instance, key, value)
            update_instance.update_time = datetime.now()
            update_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
