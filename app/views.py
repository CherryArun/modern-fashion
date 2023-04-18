from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
import datetime
from django.db.models import Q
from django.db import connection
import random 
from django.db.models import Sum, Count
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.utils import timezone
import cv2
import imutils
import numpy as np
import os

def home(request):
	product_detail = Product.objects.all()
	return render(request,'index.html',{'product_detail':product_detail})
def product_list(request):
	product_detail = Product.objects.all()
	if request.GET.get('search'):
		a = request.GET.get('search')
		detail = Product.objects.filter(Q(product_name__istartswith=a) | Q(product_name__iendswith=a))
		return render(request,'product.html',{'detail':detail})
	return render(request,'product.html',{'product_detail':product_detail})
def user_login(request):
	if request.session.has_key('user'):
		return redirect("dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('email')
			password =  request.POST.get('password')
			post = User_Detail.objects.filter(email=username,password=password)
			if post:
				username = request.POST.get('email')
				request.session['user'] = username
				a = request.session['user']
				sess = User_Detail.objects.only('id').get(email=a).id
				request.session['user_id']=sess
				return redirect("dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'login.html',{})
def dashboard(request):
	if request.session.has_key('user'):
		return render(request,'dashboard.html',{})
	else:
		return render(request,'login.html',{})
def logout(request):
    try:
        del request.session['user']
    except:
     pass
    return render(request, 'login.html', {})
def register(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		password = request.POST.get('password')
		email = request.POST.get('email')
		mobile = request.POST.get('mobile')
		city = request.POST.get('city')
		address = request.POST.get('address')
		pincode = request.POST.get('pincode')
		crt = User_Detail.objects.create(name=name,
		password=password,email=email,mobile=mobile,city=city,
		address=address,pincode=pincode)
		if crt:
			messages.success(request,'Registered Successfully')
	return render(request,'register.html',{})
def add_to_cart(request,pk):
	if request.session.has_key('user_id'):
		uid = request.session['user_id']
		user_id = User_Detail.objects.get(id=int(uid))
		product_id = Product.objects.get(id=int(pk))
		product_detail = Product.objects.filter(id=int(pk))
		if request.method == 'POST':
			price = request.GET.get('price')
			tot = request.POST.get('tot')
			tot_price = float(price)*int(tot)
			crt = Cart_Detail.objects.create(user_id=user_id,product_id=product_id,status='pending',
			tot=tot,tot_price=tot_price)
			if crt:
				return redirect('view_items_cart_product')
		return render(request,'add_to_cart.html',{'product_detail':product_detail})
	else:
		return render(request,'login.html',{})
def remove_item(request,pk):
	Cart_Detail.objects.filter(id=int(pk)).delete()
	return redirect('view_items_cart_product')
def view_items_cart_product(request):
	uid = request.session['user_id']
	r_num =  random.randrange(20, 50, 3)
	product_details = Cart_Detail.objects.filter(status='pending',user_id=int(uid))
	tot = Cart_Detail.objects.filter(status='pending',user_id=int(uid)).aggregate(Sum('tot_price'))
	return render(request,'view_items_cart_product.html',{'product_details':product_details,'tot':tot,'r_num':r_num})
def purchase(request):
	uid = request.session['user_id']
	order_id =  request.GET.get('order_id')
	amount = request.GET.get('tot')
	addr = User_Detail.objects.filter(id=int(uid))
	if request.method == 'POST':
		email = request.POST.get('email')
		o_id = request.POST.get('order_id')
		total = request.POST.get('tot')
		recipient_list = [email]
		email_from = settings.EMAIL_HOST_USER
		b = EmailMessage('Order is Placed Successfully.','Order ID:'+ o_id +  'Total Amount: Rs'+ total ,email_from,recipient_list).send()
		upd = Cart_Detail.objects.filter(user_id=int(uid),status='pending').update(status='order',book_id=order_id,date=timezone.now())
		if upd:
			return redirect('order_item_user')
	return render(request,'purchase.html',{'addr':addr})
def order_item_user(request):
	uid = request.session['user_id']
	cursor = connection.cursor()
	post = '''SELECT Sum(app_cart_detail.tot_price), app_cart_detail.book_id, app_cart_detail.date, app_cart_detail.status,
	app_cart_detail.user_id_id  from app_cart_detail where app_cart_detail.status='order' OR app_cart_detail.status='paid' AND 
	app_cart_detail.user_id_id = '%d' Group By app_cart_detail.book_id  '''  % (int(uid))
	query = cursor.execute(post)
	row = cursor.fetchall()
	return render(request,'order_item_user.html',{'product_details':row})
def purchased_item(request,pk,status):
	uid = request.session['user_id']
	product_details = Cart_Detail.objects.filter(book_id=pk,user_id=int(uid))
	tot = Cart_Detail.objects.filter(book_id=pk,user_id=int(uid)).aggregate(Sum('tot_price'))
	return render(request,'purchased_item.html',{'product_details':product_details,'tot':tot,'status':status})
def loadImages():
	directory = os.getcwd()
	file_name = directory+"/media/product/"
	folder = file_name
	images = []
	thres = [140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140]
	for filename in os.listdir(folder):
		img = cv2.imread(os.path.join(folder, filename))
		if img is not None:
			images.append(img)
	return images
def virtual():
    cap = cv2.VideoCapture(0)
    images = loadImages()
    thres = [140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140]
    size = 180
    curClothId = 1
    th = thres[0]
    while True:
        (ret, cam) = cap.read()
        cam = cv2.flip(cam, 1, 0)
        t_shirt = images[curClothId]
        resized = imutils.resize(cam, width=800)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                # only works if circle of radius 30 exists
                if r > 30:
                    # draw circle and center of circle contour
                   
                    
                    # adjust size of tshirt according to radius of circle
                    size = r * 7
        if size > 350:
            size = 350
        elif size < 100:
            size = 100

        t_shirt = imutils.resize(t_shirt, width=size)

        f_height = cam.shape[0]
        f_width = cam.shape[1]
        t_height = t_shirt.shape[0]
        t_width = t_shirt.shape[1]
        height = int(f_height / 2 - t_height / 2)
        width = int(f_width / 2 - t_width / 2)
        rows, cols, channels = t_shirt.shape
        t_shirt_gray = cv2.cvtColor(t_shirt, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(t_shirt_gray, th, 255, cv2.THRESH_BINARY_INV)
        mask_inv = cv2.bitwise_not(mask)
        roi = cam[height:height + t_height, width:width + t_width]
        img_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        img_fg = cv2.bitwise_and(t_shirt, t_shirt, mask=mask)

        t_shirt = cv2.add(img_bg, img_fg)
        # cv2.imshow("tshirt", mask)

        cam[height:height + t_height, width:width + t_width] = t_shirt
        font = cv2.FONT_HERSHEY_PLAIN  # Creates a font
        x = 10  # position of text
        y = 20  # position of text

        cv2.putText(cam, "press 'n' key for next item, 'p' for previous ", (x, y), font, .8, (255, 255, 255),
                    1)  # Draw the text
        cv2.namedWindow("Modern Fashion Recommendation", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Modern Fashion Recommendation", int(cam.shape[1] * 1.4), int(cam.shape[0] * 1.4))
        cv2.imshow('Modern Fashion Recommendation', cam)
        key = cv2.waitKey(10)
        if key & 0xFF == ord('n'):
            if curClothId == len(images) - 1:
                print("image out of bound")
            else:
                curClothId += 1
                th = thres[curClothId]
        if key & 0xFF == ord('c'):  # save on pressing 'y'
            rand = random.randint(1, 999999)

            cv2.imwrite('output/'+str(rand)+'.png', cam)

        if key & 0xFF == ord('p'):
            if curClothId == -1:
                print("image out of bound")
            else:
                curClothId -= 1

        if key == 27:
            break
    return
def try_now(request):
	if request.session.has_key('user'):
		virtual()
		return render(request, 'try_now.html', {})
	else:
		return render(request, 'login.html', {})
def all_category(request):
	if request.session.has_key('user'):
		row = Product_Category.objects.all()
		return render(request, 'all_category.html', {'row':row})
	else:
		return render(request, 'login.html', {})
def category_list(request,pk):
	product_detail = Product.objects.filter(category=pk)
	if request.GET.get('search'):
		a = request.GET.get('search')
		detail = Product.objects.filter(Q(product_name__istartswith=a) | Q(product_name__iendswith=a))
		return render(request,'cat_product.html',{'detail':detail})
	return render(request,'cat_product.html',{'product_detail':product_detail})