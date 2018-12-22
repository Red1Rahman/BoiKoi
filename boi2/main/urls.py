from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
        url(r'^$', views.welcome, name='welcome'),

        url(r'^home/$', views.home, name='home'),

        # account authentications
        url(r'^signup/$', views.signup, name='signup'),
        url(r'^signin/$', views.signin, name='signin'),
        url(r'^logout/$', views.logoutview, name='logout'),

        # showing user's wall
        url(r'^wall/(?P<user_name>[0-9a-zA-Z\_\.]+)/$', views.wallview, name='wall'),
        # showing book page
        url(r'^book/(?P<book_id>[0-9]+)/$', views.bookview, name='book'),
        url(r'^booklist/$', views.booklistview, name='booklist'),
        # showing author's page
        url(r'^author/(?P<author_id>[0-9]+)/$', views.authorview, name='author'),
        url(r'^authorlist/$', views.authorlistview, name='authorlist'),

        # adding to donation list
        url(r'^addgive/$', views.addgivelistingview, name='addgive'),
        # adding to wishlist
        url(r'^addtake/$', views.addtakelistingview, name='addtake'),

        # for transferring books
        # requesting book
        url(r'^profile/requests/(?P<list_id>[0-9a-zA-Z]+)/(?P<donor>[0-9a-zA-Z]+)/for/(?P<book_id>[0-9a-zA-Z]+)/$',
            views.requestbook, name='requestbook'),
        url(r'^donate/(?P<requestor>[0-9a-zA-Z]+)/for/(?P<book_id>[0-9a-zA-Z]+)/(?P<answer>[a-zA-Z]+)/$',
            views.donate, name='donate'),

        # showing profile info
        url(r'^profile/(?P<user_name>[a-zA-Z0-9\_\.]+)/$', views.profile, name='profilepage'),
        # for editing profile info
        url(r'^profile/(?P<user_name>[0-9a-zA-Z\_\.]+)/Edit/$', views.editpage, name='editPage'),
        url(r'^saveEdit/$', views.editinfo, name='editinfo'),
        # uploading user image
        url(r'^uploadDP/$', views.upload_image, name='uploadDP'),

        # for search
        url(r'^searchRequest/$', views.search, name='search'),

        # for seeing detailed post
        url(r'^post/(?P<post_id>[0-9]+)/$', views.postview, name='postpage'),
        # for commenting
        url(r'^comment/(?P<post_id>[0-9]+)/$', views.commentview, name='like'),
        # for liking
        url(r'^like/(?P<post_id>[0-9]+)/$', views.likeview, name='like'),

        # for messaging
        url(r'^messages/$', views.messageview, name='message'),
        url(r'^loadmessage/(?P<user_id>[0-9]+)/$', views.messageloaderview, name='messageloader'),
        url(r'^postmessage/(?P<user_id>[0-9]+)/$', views.sendmessageview, name='messageposter'),

        # for hub
        url(r'^hub/$', views.hubview, name='hub'),

]

