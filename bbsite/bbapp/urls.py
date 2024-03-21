from django.urls import path, re_path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.BulletsHome.as_view(), name='home'),  # http://127.0.0.1:8000
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<int:pk>/', views.ShowPosts.as_view(), name='post'),
    path('comments/<int:pk>/', views.ShowUserComments.as_view(), name='comments_user'),
    path('<int:pk>/addcomment/', views.CreateComment.as_view(), name='add_comment'),
    path('category/<int:pk>/', views.BulletsCategory.as_view(), name='category'),
    path('<int:pk>/edit/', views.EditPage.as_view(), name='edit_page'),
    path('<int:pk>/delete/', views.DeletePage.as_view(), name='delete_page'),
]
