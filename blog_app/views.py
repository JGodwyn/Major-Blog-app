import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from .models import User, Posts, LikedPost
import datetime
from django.core.files.storage import FileSystemStorage

all_categories = ['Health', 'Code', 'Lifestyle', 'Abstract', 'Comic and characters', 'Business', 'Games', 'Music', 'Religion', 'Sales']  # all the categories to choose when you signup, you can add or remove from it
category_chosen = True
name_exists = False


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
    main_user_object = get_object_or_404(User, id=line_id)  # the person's profile you are in !
    all_post = Posts.objects.all().order_by('-date_created')   # all the posts in the database
    liked_posts = []  # the list i would put the liked posts
    for line in main_user_object.liked_list.all():
        liked_posts.append(Posts.objects.get(id = line.liked_post_id))

    # think about making this a function, that can be called by any page
    if request.method == 'POST':
        try:
            if request.POST.get('search'):
                searched_text = request.POST.get('search')
                return HttpResponseRedirect(reverse('blog:dashboard_search', args = (line_id, searched_text)))
            else:
                post_user = int(request.POST.get('post_user'))
                user_object = get_object_or_404(User, id = post_user)   # the user whose post is liked
                post_id = int(request.POST.get('post_id'))
                post_object = user_object.post.get(id=post_id)  # the post

                # FOR LIKES

                if not main_user_object.liked_list.all():  # no object in the list
                    main_user_object.liked_list.create(liked_post_id = post_object.id)
                    post_object.likes += 1
                    post_object.save()
                    main_user_object.save()

                else:
                    for entry in main_user_object.liked_list.all():  # object present in the list
                        if post_object.id == entry.liked_post_id:
                            entry.delete()
                            post_object.likes -= 1
                            main_user_object.save()
                            post_object.save()
                            break

                        else:
                            if entry != main_user_object.liked_list.all().last():
                                continue

                            if post_object.id == entry.liked_post_id:
                                entry.delete()
                                post_object.likes -= 1
                                main_user_object.save()
                                post_object.save()
                                break

                            added = main_user_object.liked_list.create(liked_post_id = post_object.id)
                            post_object.likes += 1
                            main_user_object.save()
                            post_object.save()

        except TypeError:
            return HttpResponseRedirect('#')

        return HttpResponseRedirect('#')

    else:
        try:
            # the page you see when you login
            index_counter = 0
            # this is where the post generation occurs
            trial = '''def recurse():
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
            all_post_len = len(all_post)'''

            return render(request, 'blog/dashboard.html', {
                'user_object': main_user_object,
                'all_users': User.objects.all(),
                'all_post': all_post,
                'all_post_len': len(all_post),
                'liked_posts': liked_posts,
            })

        except ValueError:
            return render(request, 'blog/home.html')


def dashboard_search(request, line_id, searched_text):
    liked_posts = []
    main_user_object = get_object_or_404(User, id=line_id)  # the person's profile you are in !
    for line in main_user_object.liked_list.all():
        liked_posts.append(Posts.objects.get(id = line.liked_post_id))

    if request.method == 'POST':
        all_post = Posts.objects.all().order_by('-date_created')   # all the posts in the database
        post_user = int(request.POST.get('post_user'))
        user_object = get_object_or_404(User, id = post_user)   # the user whose post is liked
        post_id = int(request.POST.get('post_id'))
        post_object = user_object.post.get(id=post_id)

        # FOR LIKES

        if not main_user_object.liked_list.all():  # no object in the list
            main_user_object.liked_list.create(liked_post_id = post_object.id)
            post_object.likes += 1
            main_user_object.save()
            post_object.save()

        else:
            for entry in main_user_object.liked_list.all():  # object present in the list
                if post_object.id == entry.liked_post_id:
                    entry.delete()
                    post_object.likes -= 1
                    main_user_object.save()
                    post_object.save()
                    break

                else:
                    if entry != main_user_object.liked_list.all().last():
                        continue

                    if post_object.id == entry.liked_post_id:
                        entry.delete()
                        post_object.likes -= 1
                        main_user_object.save()
                        post_object.save()
                        break

                    added = main_user_object.liked_list.create(liked_post_id = post_object.id)
                    post_object.likes += 1
                    main_user_object.save()
                    post_object.save()

        return HttpResponseRedirect('#')
    else:
        matched_post = []
        user_object = get_object_or_404(User, id = line_id)
        for post in Posts.objects.all().order_by('-date_created'):
            if searched_text in post.title or searched_text.upper() in post.title or searched_text.lower() in post.title or searched_text.title() in post.title:  # whatever case it might be in
                matched_post.append(post)
        return render(request, 'blog/search_dashboard.html', {
            'user_object': user_object,
            'matched_post': matched_post,
            'matched_post_len': len(matched_post),
            'searched_text': searched_text,
            'liked_posts': liked_posts,
        })


def my_profile(request, user_id):
    user_object = get_object_or_404(User, id=user_id)
    user_posts = user_object.post.order_by('-date_created')
    length = len(user_posts)

    if request.method == 'POST':  # add an image
        try:
            document = request.FILES['document']
            fs = FileSystemStorage()
            fs.save(document.name, document)
            base_dir = (os.path.dirname(os.path.dirname(__file__)))
            doc_dir = os.path.join(base_dir, f'media\{str(document)}')
            static_dir = os.path.join(base_dir, f'blog_app\static\media\{str(document)}')
            user_object.image = document
            user_object.save()
            return HttpResponseRedirect('#')

        except MultiValueDictKeyError:
            return HttpResponseRedirect('#')

    else:
        return render(request, 'blog/my_profile.html', {
            'user_object': user_object,
            'posts': user_posts,
            'length': length
        })


def edit_profile(request, user_id):
    global category_chosen
    global name_exists
    user_object = get_object_or_404(User, id = user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        describe = request.POST.get('description')

        for line in User.objects.all():
            if username == line.username and username != user_object.username:
                name_exists = True
                return HttpResponseRedirect('#')
        try:
            name_exists = False
            category = ''
            cop = dict(request.POST.copy())
            cop = cop['category']
            end = (len(cop) - 1)
            for line in cop:
                if cop.index(line) == end:
                    category = category.__add__(line)
                    continue  # so that an extra ',' would not be added at the end
                category = category.__add__(line + ', ')
            user_object.categories = category
        except KeyError:
            category_chosen = False
            return HttpResponseRedirect('#')

        user_object.username = username
        user_object.password = password
        user_object.description = describe
        user_object.save()
        return HttpResponseRedirect(reverse('blog:my_profile', args = (user_id,)))

    else:
        return render(request, 'blog/edit_profile.html', {
            'user_object': user_object,
            'all_categories': all_categories,
            'category_chosen': category_chosen,
            'name_exists': name_exists,
        })


def another_profile(request, user_id, main_user_id):
    main_user_object = get_object_or_404(User, id = main_user_id)
    user_object = get_object_or_404(User, id=user_id)
    user_posts = user_object.post.order_by('-date_created')

    if request.method == 'POST':
        all_post = Posts.objects.all().order_by('-date_created')   # all the posts in the database
        post_user = int(request.POST.get('post_user'))
        user_object = get_object_or_404(User, id = post_user)   # the user whose post is liked
        post_id = int(request.POST.get('post_id'))
        post_object = user_object.post.get(id=post_id)

        # FOR LIKES

        if not main_user_object.liked_list.all():  # no object in the list
            main_user_object.liked_list.create(liked_post_id = post_object.id)
            post_object.likes += 1
            main_user_object.save()
            post_object.save()

        else:
            for entry in main_user_object.liked_list.all():  # object present in the list
                if post_object.id == entry.liked_post_id:
                    entry.delete()
                    post_object.likes -= 1
                    main_user_object.save()
                    post_object.save()
                    break

                else:
                    if entry != main_user_object.liked_list.all().last():
                        continue

                    if post_object.id == entry.liked_post_id:
                        entry.delete()
                        post_object.likes -= 1
                        main_user_object.save()
                        post_object.save()
                        break

                    added = main_user_object.liked_list.create(liked_post_id = post_object.id)
                    post_object.likes += 1
                    main_user_object.save()
                    post_object.save()

        return HttpResponseRedirect('#')

    else:  # the request type is GET
        length = len(user_posts)

        return render(request, 'blog/another_profile.html', {
            'main_user_object': main_user_object,
            'user_object': user_object,
            'posts': user_posts,
            'length': length
        })


def post(request, main_user_id, user_id, post_id):
    try:
        all_likers = []
        main_user_object = get_object_or_404(User, id = main_user_id)
        user_object = get_object_or_404(User, id=user_id)
        user_post = user_object.post.get(id = post_id)
        exact_title = user_object.post.get(id=post_id).title
        exact_post = user_object.post.get(id=post_id).post
        exact_date = user_object.post.get(id=post_id).date_created
        exact_likes = user_object.post.get(id = post_id).likes
        comment_list = user_post.commented.all()
        present = main_user_object.username in [line.commenter for line in comment_list]  # returns a boolean value, checks whether my name is part of the comment list. True: Put the delete comment button, else remove it.
        for line in LikedPost.objects.all():
            if line.liked_post_id == user_post.id:
                all_likers.append(line.liked_post_link)

        if request.method == "POST":  # if you write a comment
            if request.POST.get('del_comment'):
                return HttpResponseRedirect(reverse('blog:comment_delete', args = (main_user_id, user_id, post_id,)))
            else:
                user_post = user_object.post.get(id = post_id)
                comment = request.POST.get('comment')
                user_post.commented.create(comments = comment, commenter = main_user_object.username)
                user_post.save()
                return HttpResponseRedirect('#')

        return render(request, 'blog/post.html', {
            'main_user_object': main_user_object,
            'user_object': user_object,
            'exact_title': exact_title,
            'exact_post': exact_post,
            'exact_date': exact_date,
            'exact_likes': exact_likes,
            'comment_list': comment_list,
            'comment_list_length': len(comment_list),
            'present': present,
            'all_likers': all_likers,
        })

    except Posts.DoesNotExist:
        return HttpResponseRedirect(reverse('blog:dashboard', args=(user_object.id,)))


def comment_delete(request, main_user_id, user_id, post_id):
    try:
        main_user_object = get_object_or_404(User, id = main_user_id)
        user_object = get_object_or_404(User, id=user_id)
        user_post = user_object.post.get(id = post_id)
        exact_title = user_object.post.get(id=post_id).title
        exact_post = user_object.post.get(id=post_id).post
        exact_date = user_object.post.get(id=post_id).date_created
        exact_likes = user_object.post.get(id = post_id).likes

        if request.method == 'POST':
            try:
                cop = dict(request.POST.copy())
                cop = cop['del_comment']
                for line in cop:
                    user_post.commented.get(id = int(line)).delete()
                    user_post.save()
                return HttpResponseRedirect(reverse('blog:view_post', args = (main_user_id, user_id, post_id,)))
            except KeyError:
                return HttpResponseRedirect(reverse('blog:view_post', args = (main_user_id, user_id, post_id,)))

        comment_list = []
        for comments in user_post.commented.all():
            if comments.commenter == main_user_object.username:
                comment_list.append(comments)

        return render(request, 'blog/comment_delete.html', {
            'main_user_object': main_user_object,
            'user_object': user_object,
            'exact_title': exact_title,
            'exact_post': exact_post,
            'exact_date': exact_date,
            'exact_likes': exact_likes,
            'comment_list': comment_list,
            'comment_list_length': len(comment_list),
        })

    except Posts.DoesNotExist:
        return HttpResponseRedirect(reverse('blog:dashboard', args=(user_object.id,)))


def make_post(request, user_id):
    user_object = get_object_or_404(User, id=user_id)
    return render(request, 'blog/make_post.html', {
        'user_object': user_object
    })


def make_post_done(request, user_id):
    user_object = get_object_or_404(User, id=user_id)
    new_title = request.POST.get('title')
    new_post = request.POST.get('post')
    print(new_post.__repr__())
    new_post = new_post.replace('\t', ' ')
    new_post = new_post.replace('\n', ''
                                      '')
    print(new_post.__repr__())
    user_object.post.create(title=new_title, post=new_post)
    user_object.save()
    return HttpResponseRedirect(reverse('blog:dashboard', args=(user_object.id,)))


def edit_post(request, user_id, post_id):
    user_object = get_object_or_404(User, id=user_id)
    exact_title = user_object.post.get(id=post_id).title
    exact_post = user_object.post.get(id=post_id).post

    if request.method == 'POST':
        user_object = get_object_or_404(User, id=user_id)
        new_title = request.POST.get('title')
        new_post = request.POST.get('post')
        post_object = user_object.post.get(id=post_id)
        post_object.title = new_title
        post_object.post = new_post
        post_object.save()
        user_object.save()

        return HttpResponseRedirect(reverse('blog:my_profile', args = (user_id,)))

    return render(request, 'blog/edit_post.html', {
        'user_object': user_object,
        'exact_title': exact_title,
        'exact_post': exact_post,
    })


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
    user_object = get_object_or_404(User, id=user_id)
    del_this = user_object.post.get(id=post_id)
    user_object.post.get(id=post_id).delete()
    user_object.save()

    return HttpResponseRedirect(reverse('blog:my_profile', args=(user_id,)))


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
        'categories': all_categories
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
                category = category.__add__(line)
                continue  # so that an extra ',' would not be added at the end
            category = category.__add__(line + ', ')
        user_object.categories = category
        user_object.save()

        return HttpResponseRedirect(reverse('blog:description', args=(user_object.id,)))

    except KeyError:
        return render(request, 'blog/categories.html', {
            'user_object': user_object,
            'categories': all_categories,
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


def about(request):
    # display the about page
    return render(request, 'blog/about.html')


def comment_about(request):
    try:
        comment = request.POST.get('text')
        mycomments = open('comments.txt', 'a')
        mycomments.write(f'{comment}  >>>  {datetime.datetime.now().ctime()}')
        mycomments.write('\n')
        mycomments.close()
        return HttpResponseRedirect(reverse('blog:about'))
    except UnicodeEncodeError:
        return HttpResponseRedirect(reverse('blog:about'))
