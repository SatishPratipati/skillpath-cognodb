from django.shortcuts import render
from .services.graph_service import GraphService, GraphDatabaseError

def home(request):
    return render(request, "home.html")

def explore(request):
    skill = request.GET.get("skill", "").strip()
    data = None
    error = None
    if skill:
        try:
            data = GraphService().explore_skill(skill)
        except GraphDatabaseError as exc:
            error = str(exc)
    return render(request, "explore.html", {"skill": skill, "data": data, "error": error})

def career_path(request):
    start = request.GET.get("start", "").strip()
    role = request.GET.get("role", "").strip()
    data = None
    error = None
    if start and role:
        try:
            data = GraphService().find_career_path(start, role)
        except GraphDatabaseError as exc:
            error = str(exc)
    return render(request, "path.html", {"start": start, "role": role, "data": data, "error": error})
