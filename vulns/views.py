from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Note


@login_required
def index(request):
    notes = Note.objects.filter(owner=request.user)
    rendernotes = ['<span><li style="background-color: {}">{}</li></span>'.format(note.colour, note.text) for note in notes]
    return render(request, "index.html", {"notes":rendernotes,"currentuser":request.user})


@login_required
def addnote(request):
    user = User.objects.get(username=request.GET.get("user"))
    text = request.GET.get("note")
    colour = request.GET.get("colour")
    note = Note(owner=user, text=text, colour=colour)
    note.save()
    return redirect("/")


@login_required
def deletenote(request):
    text = request.GET.get("note")
    if not text:
        return redirect("/")
    notes = Note.objects.raw("SELECT * FROM vulns_note WHERE owner_id = {} AND text LIKE '%{}%'".format(request.user.id, text))
    for note in notes:
        note.delete()
    return redirect("/")