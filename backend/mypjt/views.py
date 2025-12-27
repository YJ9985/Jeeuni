from django.http import JsonResponse

def health(_):
    return JsonResponse({"ok": True})
