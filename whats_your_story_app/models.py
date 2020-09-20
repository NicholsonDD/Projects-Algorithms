from django.db import models

from datetime import date, datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def validate(self, postData):
    
        errors={}
        
        if len(postData['first_name'])< 1:
            errors['first_name']="First name must be at least two characters."
        
        if len(postData['last_name'])< 1:
            errors['last_name']="Last name must be at least two characters."
                    
        if postData['birthdate'] == '':
            errors['birthdate']= "Please choose a date."
              
        else:
            converted_date = datetime.strptime(postData['birthdate'], '%Y-%m-%d')
            if converted_date > datetime.now():
                errors['birthdate']="Invalid Date - must be in the past."


        if postData['email'] == "":
            errors['email']= "Please input your email address."
    
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="Invalid email address!"
        
        existing_emails = User.objects.filter(email=postData['email'])
        if len(existing_emails) > 0:
            errors['email']="This email is already in use."  

        if len(postData['password']) < 5:
            errors['password']="Password must be at five characters."

        if postData['password'] != postData['confirm_pwd']:
            errors['confirm_pwd']= "Confirm password does match password."

        return errors


    def validate_login(self, postData):

        errors = {}

        if postData['email'] == "":
            errors['email']= "Please input your email address."
    
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="Invalid email address!"

        if len(postData['password']) < 5:
            errors['password']="Password must be at five characters."

        
        return errors                 





class User(models.Model):

    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    birthdate = models.DateField(null=True)
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()




# NEED TO LIMIT THE NUMBER OF CHARACTERS

class StoryManager(models.Manager):

    def story_validate(self, postData):
    
        errors={}

        if postData['story_title']== "":
            errors['story_title'] = "Please choose a story title."


        existing_story_titles = Story.objects.filter(story_title = postData['story_title'])
        if len(existing_story_titles) > 0:
            errors['story_title']="This story title is already in use."  


        if len(postData['desc'])< 3:
            errors['desc']="The description must be at 3 characters long."
    
        return errors

#Limit characters for details and capitons & Make pic/cap 2 and pic/cap 3 optionaal
        
class Story(models.Model):
    story_title = models.CharField(max_length = 255)
    desc = models.TextField(max_length = 2000)
    published_by = models.ForeignKey(User, related_name="stories_created", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_stories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.story_title

    objects =StoryManager()


class Story_Image(models.Model):
    # MEDIA_ROOT is valid approach, however if we run into walls, we have options
        # Option A) External hosting, host images to Amazon or Imgur and store image links
        # Option B) Static content, upload placeholder images related to stories for demo purposes
    story_pic = models.ImageField(upload_to='images/')
    story_cap = models.CharField(max_length=255)
    story = models.ForeignKey(Story, related_name="story_images", on_delete=models.CASCADE)
    #Other users need to show th


class Comment(models.Model):
    story = models.ForeignKey(Story, related_name="has_comments", on_delete = models.CASCADE)
    commenter = models.ForeignKey(User, related_name="comments_created", on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
