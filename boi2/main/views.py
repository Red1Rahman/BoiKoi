from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.urls import reverse
from isbnlib import *
from fuzzywuzzy import fuzz
from django.db.models import Q
import operator


def welcome(request):
    return render(request, 'main/welcome.html')


def home(request):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    return redirect(reverse('main:wall', args=[request.user.username]))


def signup(request):
    form = RegisterForm()
    context = {'form': form}

    if request.method == "GET":
        return render(request, 'main/signup.html', context)

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            #return HttpResponse("<h1>username</h1><h1>password</h1><h1>email</h1>")
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('main:wall', args=[request.user.username]))
                else:
                    print("111")
            else:
                print("222")
        else:
            print("333")
        return render(request, 'main/signup.html', context)


def signin(request):
    context = {
        'success': True,
    }
    if request.method == "GET":
        return render(request, 'main/signin.html', context)
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('main:wall', args=[request.user.username]))
            else:
                print("Active na")
                return HttpResponse("Active na")
        else:
            print("hoilona")
            res = "hoilona"
            context = {
                'success': res,
            }
            return render(request, 'main/signin.html', context)


def profile(request, user_name):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    user1 = User.objects.get(username=user_name)
    profile1 = Profile.objects.get(user=user1)
    form = UploadImage()
    context = {
        'user_profile': profile1,
        'form': form,
    }

    return render(request, 'main/profile.html', context)


def wallview(request, user_name):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    user = get_object_or_404(User, username=user_name)
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        posttitle = request.POST.get('posttitle', '')
        posttext = request.POST.get('posttext', '')
        coverform = UploadCover(request.POST, request.FILES)
        files = request.FILES.getlist('cover')
        post = WallPost.objects.create(user=user, title=posttitle, text=posttext)
        post.save()
        if coverform.is_valid:
            for f in files:
                post.cover = f
            post.save()
            print(post.cover.url)

    gives = Listing.objects.filter(user=user, mode="Give", locked=False)
    takes = Listing.objects.filter(user=user, mode="Take", locked=False)
    posts = WallPost.objects.filter(user=user).order_by('-creationDate')
    requestedNotifications = RequestLog.objects.filter(donor=profile)
    requestingNotifications = RequestLog.objects.filter(requestor=profile)
    donatedbooks = TransferLog.objects.filter(provider=profile)
    receivedbooks = TransferLog.objects.filter(receiver=profile)
    denial = []
    success = []
    for mes in ServerMessage.objects.all():
        if mes.recipient == request.user and mes.mode == "denial":
            denial.append(mes)
            mes.delete()

    for mes in ServerMessage.objects.all():
        if mes.recipient == request.user and mes.mode == "success":
            success.append(mes)
            mes.delete()

    form = UploadCover()

    post_likes = []

    for post in posts:
        likeno = len(Like.objects.filter(post=post))
        print(post.title + " " + str(likeno))
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            post_likes.append([post, 'False', likeno])
            like.delete()
        else:
            post_likes.append([post, 'True', likeno])

    context = {
        'user': user,
        'gives': gives,
        'takes': takes,
        'post_likes': post_likes,
        'requested': requestedNotifications,
        'myrequests': requestingNotifications,
        'donated': donatedbooks,
        'received': receivedbooks,
        'form': form,
        'denial': denial,
        'success': success,
    }

    return render(request, 'main/wall.html', context)


def getbooklistkey(book):
    return book.name


def booklistview(request):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    booklist = []
    for book in Book.objects.all():
        booklist.append(book)

    sorted(booklist, key=getbooklistkey)
    context = {
        'booklist': booklist,
    }
    return render(request, 'main/BookList.html', context)


def bookview(request, book_id):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    book = get_object_or_404(Book, id=book_id)
    givers = Listing.objects.filter(book=book, mode="Give", locked=False)
    takers = Listing.objects.filter(book=book, mode="Take", locked=False)
    user1 = request.user
    profile1 = Profile.objects.get(user=user1)
    context = {
        'book': book,
        'givers': givers,
        'takers': takers,
        'user_profile': profile1,
    }

    return render(request, 'main/book.html', context)


def getauthorlistkey(author):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    return author.name


def authorlistview(request):
    authorlist = []
    for author in Author.objects.all():
        authorlist.append(author)

    sorted(authorlist, key=getauthorlistkey)
    context = {
        'authorlist': authorlist,
    }
    return render(request, 'main/AuthorList.html', context)


def authorview(request, author_id):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    author = get_object_or_404(Author, id=author_id)
    writtenbooks = Book.objects.filter(author=author)
    context = {
        'author': author,
        'books': writtenbooks,
    }

    return render(request, 'main/author.html', context)


def addgivelistingview(request):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == "POST":
        bookname = request.POST.get('bookname', '')
        isbn = request.POST.get('isbn', '')

        cisbn = canonical(isbn)
        book = meta(cisbn)

        if(book['Title'] == bookname):
            authorname = book['Authors'][0]
            print(authorname)

            author, created = Author.objects.get_or_create(name = authorname)

            if created:
                author.save()

            dbook, created = Book.objects.get_or_create(name = bookname, ISBN=isbn, author = author)

            if created:
                dbook.save()

            listing = Listing.objects.create(user=request.user, book=dbook, amount=1, mode="Give")
            listing.save()

        else:
            return HttpResponse("Book title doesnt match ISBN" + ". Actual book title; " + book['Title'])

        return redirect(reverse('main:wall', args = [request.user.username]))

    return render(request, 'main/addgive.html')


def addtakelistingview(request):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == "POST":
        bookname = request.POST.get('bookname', '')
        isbn = request.POST.get('isbn', '')

        cisbn = canonical(isbn)
        book = meta(cisbn)

        if(book['Title'] == bookname):
            authorname = book['Authors'][0]
            print(authorname)

            author, created = Author.objects.get_or_create(name=authorname)

            if created:
                author.save()

            dbook, created = Book.objects.get_or_create(name=bookname, ISBN=isbn, author=author)

            if created:
                dbook.save()

            listing = Listing.objects.create(user=request.user, book=dbook, amount=1, mode="Take")
            listing.save()

        else:
            return HttpResponse("Book title doesnt match ISBN" + ". Actual book title; " + book['Title'])

        return redirect(reverse('main:wall', args = [request.user.username]))

    return render(request, 'main/addtake.html')


def upload_image(request):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == "POST":
        form = UploadImage(request.POST)
        files = request.FILES.getlist('profilepic')
        if form.is_valid:
            user1 = request.user
            print(user1)
            profile1 =Profile.objects.get(user=user1)
            for f in files:
                profile1.profilepic = f
            profile1.save()
            print(profile1.profilepic.url)
            return redirect(reverse('main:profilepage', args=[request.user.username]))


def editpage(request, user_name):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    user1 = User.objects.get(username=user_name)
    profile1 = Profile.objects.get(user=user1)
    context = {
        'user_profile': profile1
    }
    return render(request, 'main/editpage.html', context)


def editinfo(request):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == "GET":
        return reverse('main:editPage', args=[request.user.username])

    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        bio = request.POST.get('bio', '')
        user1 = request.user
        profile1 = Profile.objects.get(user=user1)
        user1.username = username
        user1.email = email
        user1.save()
        profile1.user = user1
        profile1.bio = bio
        profile1.address = address
        profile1.save()
        print(request.user.username)
        return redirect(reverse('main:profilepage', args=[request.user.username]))


def search(request):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == 'POST':
        param = request.POST.get('searchReq', '')
        bookmatch = []
        usermatch = []
        postmatch = []
        for book1 in Book.objects.all():
            if book1.author:
                str1 = book1.name + book1.author.name + book1.ISBN
            else:
                str1 = book1.name + book1.ISBN
            score2 = fuzz.partial_ratio(str1.lower(), param.lower())
            if score2 > 50:
                bookmatch.append(book1)

        for prof1 in Profile.objects.all():
            str1 = prof1.user.username + prof1.user.email
            score2 = fuzz.partial_ratio(str1.lower(), param.lower())
            if score2 > 50:
                usermatch.append(prof1)

        for post in WallPost.objects.all():
            score2 = fuzz.partial_ratio(post.title.lower(), param.lower())
            if score2 > 50:
                print(post.title)
                postmatch.append(post)
                if post.user.profile not in usermatch:
                    usermatch.append(post.user.profile)

        postmatch.reverse()
        usermatch.reverse()
        bookmatch.reverse()
        context = {
            'bookmatch': bookmatch,
            'usermatch': usermatch,
            'postmatch': postmatch,
        }
        return render(request, 'main/searchResult.html', context)


def requestbook(request, list_id, donor, book_id):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    requestor1 = Profile.objects.get(user=request.user)
    user1 = User.objects.get(username=donor)
    sender = Profile.objects.get(user=user1)
    book1 = Book.objects.get(pk=book_id)
    listing = Listing.objects.get(pk=list_id)
    listing.locked = True
    listing.save()
    listing = Listing.objects.get(user=request.user, book=book1)
    listing.locked = True
    listing.save()
    newEntry = RequestLog(donor=sender, requestor=requestor1, book=book1)
    newEntry.save()
    return redirect(reverse('main:book', args=[book1.id]))


def donate(request, requestor, book_id, answer):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    user1 = User.objects.get(username=requestor)
    requestor1 = Profile.objects.get(user=user1)
    user1 = request.user
    donor1 = Profile.objects.get(user=user1)
    book1 = Book.objects.get(pk=book_id)
    if answer == 'YES':
        oldEntry = RequestLog.objects.get(donor=donor1, requestor=requestor1, book=book1)
        oldEntry.delete()
        oldEntry = ServerMessage(recipient=requestor1.user, book=book1, mode="success")
        oldEntry.save()
        listing = Listing.objects.get(user=donor1.user, book=book1)
        listing.delete()
        listing = Listing.objects.get(user=requestor1.user, book=book1)
        listing.delete()
        newEntry = TransferLog(provider=donor1, receiver=requestor1, book=book1)
        newEntry.save()
    elif answer == 'NO':
        oldEntry = RequestLog.objects.get(donor=donor1, requestor=requestor1, book=book1)
        oldEntry.delete()
        oldEntry = ServerMessage(recipient=requestor1.user, book=book1, mode="denial")
        oldEntry.save()
        listing = Listing.objects.get(user=donor1.user, book=book1)
        listing.locked = False
        listing.save()
        listing = Listing.objects.get(user=requestor1.user, book=book1)
        listing.locked = False
        listing.save()

    return redirect(reverse('main:wall', args=[request.user.username]))


def likeview(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == 'POST':
        post = WallPost.objects.get(pk=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            like.save()
            likeno = len(Like.objects.filter(post=post))
            return HttpResponse("<i class=\"fa fa-thumbs-down\"></i> Unlike " + str(likeno))
        else:
            like.delete()
            likeno = len(Like.objects.filter(post=post))
            return HttpResponse("<i class=\"fa fa-thumbs-up\"></i> Like " + str(likeno))

    else:
        return HttpResponse("Bad Request")


def postview(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    post = WallPost.objects.get(pk=post_id)

    post_like = []
    comments = Comment.objects.filter(post=post)

    likeno = len(Like.objects.filter(post=post))
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        post_like.append([post, 'False', likeno])
        like.delete()
    else:
        post_like.append([post, 'True', likeno])
    context = {
        'post': post_like,
        'comments': comments,
    }

    return render(request, 'main/postpage.html', context)


def coverupload(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == "POST":
        form = UploadImage(request.POST)
        files = request.FILES.getlist()
        if form.is_valid:
            post = WallPost.object.get(pk=post_id)
            for f in files:
                post.cover = f
            post.save()
            if post.cover:
                print(post.cover.url)
            return
    else:
        return HttpResponse("Bad Request")


def logoutview(request):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    logout(request)
    return redirect(reverse('main:signin', args=[]))


def commentview(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == 'POST':
        post = WallPost.objects.get(pk=post_id)
        text = request.body
        comment = Comment.objects.create(user = request.user, post = post, text=text)
        commentno = len(Comment.objects.filter(post = post))
        dpurl = str(comment.user.profile.profilepic.url)
        username = str(comment.user.username)
        text = str(comment.text, 'utf-8')
        comment.save()
        dict = [dpurl, username, text, commentno]
        return JsonResponse(dict, safe=False)
    else:
        return HttpResponse("Bad Request")


def messageview(request):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    allmessages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))

    received_users = allmessages.values('sender').distinct().exclude(sender=request.user)
    sent_users = allmessages.values('receiver').distinct().exclude(receiver=request.user)

    user_set = []

    for i in received_users:
        if i['sender'] not in user_set:
            user_set.append(i['sender'])

    for i in sent_users:
        if i['receiver'] not in user_set:
            user_set.append(i['receiver'])

    print(user_set)

    message_vector =[]

    for cuser in user_set:
        messages = allmessages.filter(Q(sender=cuser) | Q(receiver=cuser)).order_by('-time')
        print(str(cuser) + " " + str(messages.count()))

        if messages.count() > 0:
            lt = Message()
            lt = messages[0]
            tt = lt.text
            tt = tt[0:107]
            lt.text = tt + "..."

            if messages[0].sender.id == cuser:
                message_vector.append(lt)
            elif messages[0].receiver.id == cuser:
                message_vector.append(lt)

    message_vector = sorted(message_vector, key=lambda obj: obj.time, reverse=True)

    print(message_vector)

    context = {'newmessages' : message_vector, }

    return render(request, 'main/messages.html', context)


def messageloaderview(request, user_id):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == 'POST':
        cuser = User.objects.get(pk=user_id)
        print("should load messages for " + cuser.username)
        messagelist = Message.objects.filter(Q(sender=request.user, receiver = cuser) | Q(receiver=request.user, sender = cuser)).order_by('-time')[:50]
        messagelist = sorted(messagelist, key = lambda obj: obj.time, reverse = False)

        list = []

        for messageitem in messagelist:
            if messageitem.sender == cuser:
                dict = {'mode' : "received", 'text' :  messageitem.text, 'time' : messageitem.time, }
            elif messageitem.receiver == cuser:
                dict = {'mode': "sent", 'text': messageitem.text, 'time': messageitem.time, }

            list.append(dict)

        masterdict = {

            'user1dp': request.user.profile.profilepic.url,
            'user2dp': cuser.profile.profilepic.url,
            'messagelist': list,
            'participant': cuser.username,
            'userid': cuser.id,
        }

        return JsonResponse(masterdict, safe=False)

    else:
        return HttpResponse("Bad Request")


def sendmessageview(request, user_id):
    if not request.user.is_authenticated():
        return render(request, 'main/signin.html')
    if request.method == 'POST':
        cuser = User.objects.get(pk=user_id)
        text = request.POST.get('message', '')

        message = Message.objects.create(sender=request.user, receiver=cuser, text=text)
        message.save()

        return redirect(reverse('main:message', args=[]))
    else:
        return HttpResponse("Bad Request")


def hubview(request):
    posts = WallPost.objects.all().order_by('-creationDate')[:100]
    post_likes = []
    alllistings = Listing.objects.all()
    alllistings = sorted(alllistings, key=lambda obj: (obj.date, obj.id), reverse=True)
    sendlistings = alllistings[:15]

    bookcounter = {}

    for listing in alllistings:
        book = Book.objects.get(pk=listing.book.id)
        if bookcounter.get(book.id) is None:
            bookcounter[book.id] = 1
        else:
            bookcounter[book.id] = bookcounter[book.id]+1


    sorted_bookcounter = sorted(bookcounter.items(), key = operator.itemgetter(1), reverse=True)[:10]

    booklist = []

    for item in sorted_bookcounter:
        book = Book.objects.get(pk=item[0])
        booklist.append(book)

    print(booklist)

    for post in posts:
        likeno = len(Like.objects.filter(post=post))
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        continued = 0

        if len(post.text) > 500:
            content = str(post.text)
            content = content[0:481]
            content = content + "....."
            post.text = content
            continued = 1

        if created:
            post_likes.append([post, 'False', likeno, continued, ])
            like.delete()
        else:
            post_likes.append([post, 'True', likeno, continued, ])



    context = {'post_likes' : post_likes, 'listings' : sendlistings, 'booklist' : booklist, }
    return render(request, 'main/hub.html', context)