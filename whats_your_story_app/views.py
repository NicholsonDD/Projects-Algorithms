from django.shortcuts import render, HttpResponse, redirect
# from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .forms import StoryImageForm
from django.contrib import messages
from datetime import date,datetime
from .models import *
import bcrypt


def index(request):

    return render(request, 'index.html')

def register(request):

    errors=User.objects.validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

            return redirect('/')

    new_password = request.POST['password']
    pw_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)

    new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            birthdate =request.POST['birthdate'], 
            email=request.POST['email'],
            password=pw_hash)

    
    request.session['user'] = new_user.first_name
    request.session['id'] = new_user.id

    return redirect(f"/all_stories")

def login(request):

    errors=User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
           messages.error(request, value)

        return redirect('/')
    else:
        logged_user = User.objects.get(email=request.POST['email'])

        request.session['user'] = logged_user.first_name
        request.session['id'] = logged_user.id

        return redirect(f"/all_stories")



def profile(request):

    user = User.objects.get(id=request.session['id'])
    
    context= {

        'user' : user
    }

    return render(request, 'profile.html', context)


def all_stories(request):

    if 'user' not in request.session:
        return redirect('/')

    this_user = User.objects.get(id=request.session['id'])
    all_stories = Story.objects.all().order_by("-created_at")

    
    context = {
        
        'all_stories': all_stories,
        'this_user' : this_user

    }
    return render(request, 'storyboard.html', context)

# I can create a story with models.create, because image field is not involved
def create(request):
    if request.method == "GET":
        return render(request, 'new_story.html')
    else:
        errors = Story.objects.story_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/stories/create')
        else:
            user = User.objects.get(id=request.session['id'])
            story = Story.objects.create(
                story_title = request.POST['story_title'], 
                desc = request.POST['desc'], 
                published_by = user
            )

            return redirect(f'/stories/{story.id}/story')

  
def upload(request, id):
    user = User.objects.get(id=request.session['id'])
    story = Story.objects.get(id=id)

    if request.method == "GET":
        context = {

            'story': story,
            'user': user
        }


    if request.method == "POST":
        context = {}
        uploaded_file = request.FILES['story_pic']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)

        # NOW we are creating Image Objects with those images in the media folder
        # AND we are connecting them with a story
        new_image = Story_Image.objects.create(
            story_pic = context['url'], 
            story_cap = request.POST['story_cap'], 
            story=story
        )
        #TESTING IMAGE UPLOAD
        # print(new_image)
        # print(new_image.story_pic)

        return redirect(f'/stories/{story.id}/upload')

    return render(request,'image_edit.html', context)

def image_upload(request, id):


    if request.method == "POST":

        form = StoryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f'/story/{story.id}/image_upload')

    else:
        form =  StoryImageForm()
        context = {
            'form':form
        }   

        return render(request, 'image_edit.html', context) 


     


def image_delete(request, id, img_id):

    user = User.objects.get(id=request.session['id'])
    story = Story.objects.get(id=id)

    # story_images = Story_Image.objects.get(id=img_id)

    # story_img = Story.objects.filter(story_images=story_images).delete()

    story_img = Story_Image.objects.get(id=img_id).delete()
    
    
    return redirect(f'/all_stories')


def story(request, id):

    current_user = User.objects.get(id=request.session['id'])
    story = Story.objects.get(id=id)

    if request.method == "GET":
        context = {

            'story': story,
            'current_user': current_user
        }

        return render(request, 'story_edit.html', context)
    


def edit(request, id):
    current_user = User.objects.get(id=request.session['id'])
    story = Story.objects.get(id=id)
    if request.method == "GET":

        context = {
            'current_user': current_user,
            'story' : story
        }

        return render(request, 'story_edit.html', context)

    if request.method == "POST":

        story.story_title = request.POST['story_title']
        story.desc = request.POST['desc']

        story.save()

        return redirect(f'/stories/{story.id}/story')

def delete(request, id):
    
    user = User.objects.get(id=request.session['id'])
    destroyed = Story.objects.get(id=id)
    
    destroyed.delete()

    return redirect('/all_stories')


def like_story(request, id):

    user = User.objects.get(id=request.session['id'])
    story = Story.objects.get(id=id)

    user.liked_stories.add(story)

    return redirect('/all_stories')

def unlike_story(request, id):
    
    user = User.objects.get(id=request.session['id'])   
    story= Story.objects.get(id=id)

    user.liked_stories.remove(story)

    return redirect(f'/all_stories')

def post_comment(request, id):
    user = User.objects.get(id=request.session['id'])
    story= Story.objects.get(id=id)

        
    comment = Comment.objects.create( 
        comment=request.POST['comment'],
        commenter = user,
        story = story
    )
    return redirect('/all_stories')


def logout(request):

    request.session.flush()

    return redirect('/')

