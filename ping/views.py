import json

from django.http import HttpResponse
from .models import GroupMember
from .forms import GroupMemberForm
from django.views.decorators.csrf import csrf_exempt


def ping(request):
    return HttpResponse("Pong!")


@csrf_exempt
def create_group_member(request):
    """
    Submit in POST FORM
        form = GroupMemberForm(request.POST or None)

    if form.is_valid():
        groupmember = form.save(commit=False)
        groupmember.name = request.POST['name']
        groupmember.email = request.POST['email']
        groupmember.save()
        return HttpResponse("Group member created!")
    else:
        return HttpResponse("Form is not valid!")
    """

    # Submit in JSON
    form = GroupMemberForm()
    if request.method == 'POST':
        request_data = json.loads(request.body)
        groupmember = form.save(commit=False)
        groupmember.name = request_data['name']
        groupmember.email = request_data['email']
        groupmember.save()
        return HttpResponse("Group member created!")
    else:
        return HttpResponse("Method not allowed! Use POST and JSON instead.")
