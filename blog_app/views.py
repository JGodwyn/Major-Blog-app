from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import User, Posts, Categories


categories_list = Categories.objects.all()  # all the categories in the database
counter = 0  # this is used in the post generation in 'dashboard'
all_post = []
check_post = 0  # this is a counter that helps when i make a post, it helps add the post to the list
delete_post = 0  # this is a counter that helps when i delete a post, it helps remove the post from the list


def home(request):
    # render the homepage HTML
    return render(request, 'blog/home.html')


def verify(request):
    # you can liken this to login,
    # where the database checking against password is done

    # in the case of no users in the database,
    # this helps prevent any stupid error
    if User.objects.all():
        pass
    else:
        return render(request, 'blog/home.html',
                      {'error_message': 'Those values do not match anyone we have'})

    try:
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        count = 0
        for line in User.objects.all():
            count += 1
            if line.username == username and line.password == password:
                return HttpResponseRedirect(reverse('blog:dashboard', args=(line.id,)))
            else:
                if count == len(User.objects.all()):
                    return render(request, 'blog/home.html',
                                  {'error_message': 'Those values do not match anyone we have'})
    except ValueError:
        return render(request, 'blog/home.html',
                      {'error_message': 'Those values do not match anyone we have'})


def dashboard(request, line_id):
    try:
        # the page you see when you login
        global check_post
        global delete_post
        global all_post
        index_counter = 0

        trial = '''
        # this works but doesn't do what i want
        
        all_users = User.objects.reverse()
        all_post = []
        for user in all_users:
            for post in user.post.order_by('-date_created')[:2]:  # order by date created, give me only the last two posts
                all_post.append(post)
        '''

        # this is where the post generation occurs
        def recurse():
            # this works yet
            size_of_queryset = len(User.objects.all()) - 1
            global counter
            nonlocal index_counter

            for item in list(range(len(User.objects.all()))):
                if not check_post == 0:  # check if a post has been added
                    break
                if not delete_post == 0:  # check if a post has been deleted
                    break
                try:
                    all_post.append(
                        User.objects.all().__getitem__(item).post.all()[counter])  # this returns a post object not a string
                except IndexError:
                    index_counter += 1
                    if index_counter == len(User.objects.all()):
                        break
                    pass         # if there happen to be a index error, ignore it. This method throws a lot of index error
                except RecursionError:
                    counter = 0  # when the end of the recursion is reached, reset the counter to 0 so that this can work again if the page is refreshed
                    break

                if item == size_of_queryset:
                    counter += 1
                    index_counter = 0
                    recurse()   # go again

        recurse()
        all_post.reverse()  # reverse the flow of the list

        # this renders the post
        all_post_len = len(all_post)
        user_object = get_object_or_404(User, id=line_id)
        return render(request, 'blog/dashboard.html', {
            'user_object': user_object,
            'all_users': User.objects.all(),
            'all_post': all_post,
            'all_post_len': all_post_len,
        })

    except ValueError:
        return render(request, 'blog/home.html')


def my_profile(request, user_id):
    user_object = get_object_or_404(User, id=user_id)
    user_posts = user_object.post.order_by('-date_created')
    length = len(user_posts)

    return render(request, 'blog/my_profile.html', {
        'user_object': user_object,
        'posts': user_posts,
        'length': length
    })


def another_profile(request, user_id):
    user_object = get_object_or_404(User, id=user_id)
    user_posts = user_object.post.order_by('-date_created')
    length = len(user_posts)

    return render(request, 'blog/another_profile.html', {
        'user_object': user_object,
        'posts': user_posts,
        'length': length
    })


def post(request, user_id, post_id):
    try:
        user_object = get_object_or_404(User, id=user_id)
        exact_title = user_object.post.get(id=post_id).title
        exact_post = user_object.post.get(id=post_id).post
        exact_date = user_object.post.get(id=post_id).date_created
        return render(request, 'blog/post.html', {
            'user_object': user_object,
            'exact_title': exact_title,
            'exact_post': exact_post,
            'exact_date': exact_date,
        })

    except Posts.DoesNotExist:
        return HttpResponseRedirect(reverse('blog:dashboard', args=(user_object.id,)))


def make_post(request, user_id):
    user_object = get_object_or_404(User, id=user_id)
    return render(request, 'blog/make_post.html', {
        'user_object': user_object
    })


def make_post_done(request, user_id):
    global check_post
    check_post = 1
    user_object = get_object_or_404(User, id=user_id)
    new_title = request.POST.get('title')
    new_post = request.POST.get('post')
    all_post.append(user_object.post.create(title=new_title, post=new_post))
    return HttpResponseRedirect(reverse('blog:dashboard', args=(user_object.id,)))


def delete_post_page(request, user_id, post_id):
    user_object = get_object_or_404(User, id=user_id)
    exact_title = user_object.post.get(id=post_id).title
    exact_post = user_object.post.get(id=post_id)
    exact_date = user_object.post.get(id=post_id).date_created

    return render(request, 'blog/delete_post.html', {
        'user_object': user_object,
        'exact_title': exact_title,
        'exact_post': exact_post,
        'exact_date': exact_date,
    })


def delete_post_done(request, user_id, post_id):
    global delete_post
    delete_post = 1
    user_object = get_object_or_404(User, id=user_id)
    del_this = user_object.post.get(id=post_id)
    user_object.post.get(id = post_id).delete()
    del_this_index = all_post.index(del_this)
    user_object.save()
    all_post.pop(del_this_index)

    return HttpResponseRedirect(reverse('blog:dashboard', args=(user_id,)))


def signup(request):
    # render the sign up page
    return render(request, 'blog/signup.html')


def signed_up(request):
    # check the data put in the signup page

    # consider the case where someone signs up successfully, then goes back through the browser's back function
    # the name he used there gets saved, that should not be the case
    # it should get deleted
    # so is the case of description
    for user in User.objects.all():
        if user.categories == '' or user.description == '':
            user.delete()

    error_message1 = 'That name already exists'
    error_message2 = 'Please, check the values'

    username = request.POST.get('Username')
    password = request.POST.get('Password')

    if password.startswith(' ') or username.startswith(' ') or password == '' or username == '' or username.isdigit():
        # no username or password given
        error_message = error_message2
        return HttpResponseRedirect(reverse('blog:sign_up_failed', args=(error_message,)))

    # check if name exists
    for line in User.objects.all():
        if username == line.username:
            # name already exists in the database
            error_message = error_message1
            return HttpResponseRedirect(reverse('blog:sign_up_failed', args=(error_message,)))
    else:
        this_user = User.objects.create(username=username, password=password)
        return HttpResponseRedirect(reverse('blog:categories', args=(this_user.id,)))


def sign_up_failed(request, error_message):
    # when the signup fails
    return render(request, 'blog/sign_up_failed.html', {
        'error_message': error_message
    })


def categories(request, user_id):
    # render the category HTML page, no logic here!
    user_object = get_object_or_404(User, id=user_id)
    return render(request, 'blog/categories.html', {
        'user_object': user_object,
        'categories': categories_list
    })


def categories_verify(request, user_id):
    # check the categories chosen and pass it to the database
    user_object = get_object_or_404(User, id=user_id)

    try:
        category = ''
        cop = dict(request.POST.copy())
        cop = cop['category']
        end = (len(cop) - 1)
        for line in cop:
            if cop.index(line) == end:
                category = category.__add__(line);
                continue  # so that an extra ',' would not be added at the end
            category = category.__add__(line + ', ')
        user_object.categories = category
        user_object.save()

        return HttpResponseRedirect(reverse('blog:description', args=(user_object.id,)))

    except KeyError:
        return render(request, 'blog/categories.html', {
            'user_object': user_object,
            'categories': categories_list,
            'error_message': 'Please select at least one category'
        })


def description(request, user_id):
    # render the description HTML page
    user_object = get_object_or_404(User, id=user_id)
    return render(request, 'blog/description.html', {
        'user_object': user_object
    })


def description_done(request, user_id):
    # check the description given and pass it to the database
    this_user = get_object_or_404(User, id=user_id)
    describe_me = request.POST.get('description')
    this_user.description = describe_me
    this_user.save()
    return HttpResponseRedirect(reverse('blog:dashboard', args=(this_user.id,)))
