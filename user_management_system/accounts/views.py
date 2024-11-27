
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from .models import Role
from django.contrib.auth.decorators import login_required

User = get_user_model()



@login_required
def user_logout(request):
    logout(request)  # Log out the user
    return redirect('registration/login/')  # Redirect to login page after logout

@login_required
def home(request):
    users = User.objects.all()  # Fetch all users if needed
    roles = Role.objects.all()   # Fetch all roles
    return render(request, 'accounts/home.html', {'users': users, 'roles': roles})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})



@login_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        selected_role_id = request.POST.get('role')  # Get the selected role from the form

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        # Check if the user is a superuser
        if not request.user.is_superuser:
            # If not a superuser, assign the lowest priority role if no roles are selected
            if selected_role_id:
                role = Role.objects.get(id=selected_role_id)
                user.roles.add(role)
            else:
                # Assign the lowest priority role (create one if it doesn't exist)
                lowest_priority_role, created = Role.objects.get_or_create(
                    name='Lowest Priority',
                    defaults={'priority': 0}  # Set default priority for lowest role
                )
                user.roles.add(lowest_priority_role)
        else:
            # Superuser can assign any role or leave it unassigned
            if selected_role_id:
                role = Role.objects.get(id=selected_role_id)
                user.roles.add(role)

        return redirect('user_list')

    # Get current user's highest role priority for filtering roles
    current_user_roles = request.user.roles.all()
    current_user_highest_priority = max(
        (role.priority for role in current_user_roles), default=-1
    )

    # Filter roles to show only those with lower or equal priority
    available_roles = Role.objects.filter(priority__lte=current_user_highest_priority)
    
    return render(request, 'accounts/add_user.html', {'roles': available_roles})


@login_required
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.set_password(request.POST['password'])
        user.save()
        return redirect('user_list')
    return render(request, 'accounts/edit_user.html', {'user': user})

@login_required
def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('user_list')

@login_required
def role_list(request):
    roles = Role.objects.all()
    return render(request, 'accounts/role_list.html', {'roles': roles})



@login_required
def assign_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    roles = Role.objects.all()

    if request.method == 'POST':
        selected_roles = request.POST.getlist('roles')

        # Get current user's highest role priority
        current_user_roles = request.user.roles.all()
        current_user_highest_priority = max(
            (role.priority for role in current_user_roles), default=-1
        )

        # Check if the user being modified has roles
        user_roles = user.roles.all()
        user_highest_priority = max(
            (role.priority for role in user_roles), default=-1
        )

        # Assign new roles
        for role_id in selected_roles:
            role = get_object_or_404(Role, id=role_id)

            # If the current user is a superuser, they can assign any role
            if request.user.is_superuser:
                # Superuser can assign any role regardless of priority
                user.roles.add(role)
            elif role.priority > current_user_highest_priority:
                # Handle error: user cannot assign this role
                return render(request, 'accounts/assign_role.html', {
                    'user': user,
                    'roles': roles,
                    'error': f"You cannot assign the {role.name} role as it has a higher priority than your own."
                })
            else:
                # Assign the role if all checks pass
                user.roles.add(role)

        return redirect('user_list')  # Redirect after assignment

    return render(request, 'accounts/assign_role.html', {'user': user, 'roles': roles})


@login_required
def add_role(request):
    if request.method == 'POST':
        name = request.POST['name']
        priority = int(request.POST['priority'])

        # Check if the user has permission to create this role
        current_user_roles = request.user.roles.all()
        
        # If the current user is a superuser, they can create any priority
        if not request.user.is_superuser:
            current_user_highest_priority = max(
                (role.priority for role in current_user_roles), default=-1
            )

            if priority > current_user_highest_priority:
                # Handle error: user cannot create a role with higher priority
                return render(request, 'accounts/add_role.html', {
                    'error': "You cannot create a role with higher priority than your own."
                })

        Role.objects.create(name=name, priority=priority)
        return redirect('role_list')

    return render(request, 'accounts/add_role.html')



@login_required
def edit_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    if request.method == 'POST':
        role.name = request.POST['name']
        role.priority = int(request.POST['priority'])  # Update the priority
        role.save()
        return redirect('role_list')

    return render(request, 'accounts/edit_role.html', {'role': role})


@login_required
def delete_role(request, role_id):
    Role.objects.get(id=role_id).delete()
    return redirect('role_list')