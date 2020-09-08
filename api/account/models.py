from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from io import BytesIO
from PIL import Image
import numpy as np         # importing numpy(to solve mathematical expressions)
import cv2
# Create your models here.

class UserImages(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField()
    cartoon_image = models.ImageField(blank=True,null=True)
    uploaded_on = models.DateTimeField(auto_now=True)

    def saveCImage(self,*args,**kwargs):
        img = cv2.imread(self.image.path)
        # image processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
        gray = cv2.medianBlur(gray, 5)                  
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)  
        color = cv2.bilateralFilter(img, 9, 300, 300)      
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        # save image to UserImage instance
        c_img = Image.fromarray(cartoon,'RGB')
        stream = BytesIO()
        c_img.save(stream,'JPEG')
        file_name = f'Cartoonized_{self.id}.jpg'
        self.cartoon_image.save(file_name,File(stream),save=False)
        self.save()

    def __str__(self):
        return self.user.username
    