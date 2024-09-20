from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from products.models import Product
import re


def signin(request):
  if request.method == 'POST' and 'btn_login' in request.POST:
    
    username = request.POST['user']
    password = request.POST['pass']
    
    user = auth.authenticate(username=username, password=password)
    
    # If user created login him automatically
    if user is not None:
      if 'remember_me' not in request.POST:
        request.session.set_expiry(0)

      auth.login(request, user)
      # messages.success(request, 'Your are logged in')
    else:
      messages.error(request, 'Username or password invalid!')
    
    return redirect('signin')
  else:
    return render(request, 'accounts/signin.html')


def logout(request):
  if request.user.is_authenticated:
    auth.logout(request)
  return redirect('index')


def signup(request):
  
  if request.method == 'POST' and 'btn_signup' in request.POST:
    
    # Variables for fields
    fname = None
    lname = None
    address = None
    address2 = None
    city = None
    state = None
    zip = None
    email = None
    username = None
    password = None
    terms = None
    is_added = None
    
    # Get Values from the Form
    if 'fname' in request.POST: fname = request.POST['fname']
    else: messages.error(request, 'Error In First Name!')
    
    if 'lname' in request.POST: lname = request.POST['lname']
    else: messages.error(request, 'Error In Last Name!')
    
    if 'address' in request.POST: address = request.POST['address']
    else: messages.error(request, 'Error In address!')
    
    if 'address2' in request.POST: address2 = request.POST['address2']
    else: messages.error(request, 'Error In address2!')
    
    if 'city' in request.POST: city = request.POST['city']
    else: messages.error(request, 'Error In city!')
    
    if 'state' in request.POST: state = request.POST['state']
    else: messages.error(request, 'Error In state!')
    
    if 'zip' in request.POST: zip = request.POST['zip']
    else: messages.error(request, 'Error In zip!')
    
    if 'email' in request.POST: email = request.POST['email']
    else: messages.error(request, 'Error In Email!')
    
    if 'user' in request.POST: username = request.POST['user']
    else: messages.error(request, 'Error In UserName!')
    
    if 'pass' in request.POST: password = request.POST['pass']
    else: messages.error(request, 'Error In Password!')
    
    if 'terms' in request.POST: terms = request.POST['terms']
    
    # Check the Values
    if fname and lname and address and address2 and city and state and zip and email and username and password:
      if terms == 'on':
        # Check If UserName Is Taken
        if User.objects.filter(username=username).exists():
          messages.error(request, 'This UserName Is Taken!')
        else:
          # Check If Email Is Taken
          if User.objects.filter(email=email).exists():
            messages.error(request, 'This Email Is Taken!')
          else:
            pattern = r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
            
            if re.match(pattern, email):
              # Add User
              user = User.objects.create_user(
                first_name=fname,
                last_name=lname,
                email=email,
                username=username,
                password=password)
              
              user.save()
              
              # Add User Profile
              user_profile = UserProfile(
                user=user, 
                address=address, 
                address2=address2, 
                city=city, 
                state=state, 
                zip=zip)
              
              user_profile.save()
              
              # Clear Fields after saving
              fname = ''
              lname = ''
              address = ''
              address2 = ''
              city = ''
              state = ''
              zip = ''
              email = ''
              username = ''
              password = ''
              terms = None
              
              # Success Message
              messages.success(request, 'Your Account Is Created Successfully')
              # is_added = True only if user account is created 
              is_added = True
            else:
              messages.error(request, 'Invalid Email!')
      else:
        messages.error(request, 'You Must Agree To The Terms!')
        
    else:
      messages.error(request, 'Check Empty Fields!')
    
    return render(request, 'accounts/signup.html', {
      'fname':fname,
      'lname':lname,
      'address':address,
      'address2':address2,
      'city':city,
      'state':state,
      'zip':zip,
      'email':email,
      'user':username,
      'pass':password,
      'is_added':is_added,
      
      })
  else:
    return render(request, 'accounts/signup.html')


def profile(request):
  if request.method == 'POST' and 'btn_save' in request.POST:
    
    if request.user is not None and request.user.id != None:
      user_profile = UserProfile.objects.get(user=request.user)
      
      if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['address2'] and request.POST['city']and request.POST['state'] and request.POST['zip'] and request.POST['email'] and request.POST['user'] and request.POST['pass']:
        
        request.user.first_name = request.POST['fname']
        request.user.last_name = request.POST['lname']
        user_profile.address = request.POST['address']
        user_profile.address2 = request.POST['address2']
        user_profile.city = request.POST['city']
        user_profile.state = request.POST['state']
        user_profile.zip = request.POST['zip']
        
        # Disable email and user to prevent any manipulation in inspect section
        # request.user.email = request.POST['email']
        # request.user.username = request.POST['user']
        
        # Manage password security by 
        # making sure pass is encrypted with 'pbkdf2_sha256$' method
        # you can find it in your postgresql auth_user passwords
        if not request.POST['pass'].startswith('pbkdf2_sha256$'):
          request.user.set_password(request.POST['pass'])
        
        request.user.save()
        user_profile.save()
        auth.login(request, request.user)
        messages.success(request, 'Your data has been saved')
      
      else:
        messages.error(request, 'Check Your Values and Elements!')
        
    return redirect('profile')
  else:
    # solving profile error
    # if request.user.is_anonymous: return redirect('index')
    # if request.user.id == None: return redirect('index')
    
    if request.user is not None:
      
      context = None
      
      if not request.user.is_anonymous:
        user_profile = UserProfile.objects.get(user=request.user)
        
        context = {
          'fname':request.user.first_name,
          'lname':request.user.last_name,
          'address':user_profile.address,
          'address2':user_profile.address2,
          'city':user_profile.city,
          'state':user_profile.state,
          'zip':user_profile.zip,
          'email':request.user.email,
          'user':request.user.username,
          'pass':request.user.password,
        }
      
      return render(request, 'accounts/profile.html', context)
    else:
      return redirect('profile')


def product_favorite(request, pro_id):
  if request.user.is_authenticated and not request.user.is_anonymous:
    pro_fav = Product.objects.get(pk=pro_id)
    
    #manage not adding fav product more than once
    if UserProfile.objects.filter(user=request.user, product_favorites=pro_fav).exists():
      messages.success(request, 'Already in the favorite list!')
    else:
      user_profile = UserProfile.objects.get(user=request.user)
      user_profile.product_favorites.add(pro_fav)
      messages.success(request, 'Product has been favored')
  else:
    messages.error(request, 'You Must Be Logged In!')

  return redirect('/products/' + str(pro_id))
  
  
def show_product_favorite(request):
  context = None
  
  if request.user.is_authenticated and not request.user.is_anonymous:
    user_info = UserProfile.objects.get(user=request.user)
    pro = user_info.product_favorites.all()
    context = {
      'products':pro,
    }
    
  return render(request, 'products/products.html', context)
