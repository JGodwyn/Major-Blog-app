from django.urls import path, include
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup', views.signup, name = 'signup'),
    path('login/verify', views.verify, name = 'verify'),
    path('dashboard/<int:line_id>', views.dashboard, name = 'dashboard'),
    path('signed_up/categories/verify/<int:user_id>', views.categories_verify, name = 'categories_verify'),
    path('signed_up', views.signed_up, name = 'signed_up'),
    path('signup/failed/<str:error_message>', views.sign_up_failed, name = 'sign_up_failed'),
    path('signed_up/categories/<int:user_id>', views.categories, name = 'categories'),
    path('signed_up/description/<int:user_id>', views.description, name = 'description'),
    path('signed_up/description/done/<int:user_id>', views.description_done, name = 'description_done'),
    path('dashboard/Profile/<int:user_id>', views.my_profile, name = 'my_profile'),
    path('dashboard/Profiles/<int:user_id>', views.another_profile, name = 'another_profile'),
    path('dashboard/post/<int:user_id>/<int:post_id>', views.post, name = 'view_post'),
    path('dashboard/Make_post/<int:user_id>', views.make_post, name = 'make_post'),
    path('dashboard/Make_post/done/<int:user_id>', views.make_post_done, name = 'make_post_done'),
    path('dashboard/profile/delete/<int:user_id>/<int:post_id>', views.delete_post_page, name = 'delete_post_page'),
    path('dashboard/profile/delete/post/<int:user_id>/<int:post_id>', views.delete_post_done, name = 'delete_post_done'),

]
