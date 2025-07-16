from django.contrib.auth.models import Group, Permission


def create_groups_permission(sender, **kwargs):

    try:
        # Create Groups
        readers_group, created = Group.objects.get_or_create(name='Readers')
        authors_group, created = Group.objects.get_or_create(name='Authors')
        editors_group, created = Group.objects.get_or_create(name='Editors')
        admins_group, created = Group.objects.get_or_create(name='Admins')

        # Create Permissions
        readers_permission = [
            Permission.objects.get(codename='view_jobboard')
        ]

        authors_permission = [
            Permission.objects.get(codename='view_jobboard'),
            Permission.objects.get(codename='add_jobboard'),
        ]

        editors_permission = [
            Permission.objects.get(codename='view_jobboard'),
            Permission.objects.get(codename='add_jobboard'),
            Permission.objects.get(codename='change_jobboard'),       
        ]

        admins_permission = [
            Permission.objects.get(codename='view_jobboard'),
            Permission.objects.get(codename='add_jobboard'),
            Permission.objects.get(codename='change_jobboard'),
            Permission.objects.get(codename='delete_jobboard'),       
        ]

        # Assigning permissions to the groups

        readers_group.permissions.set(readers_permission)
        authors_group.permissions.set(authors_permission)
        editors_group.permissions.set(editors_permission)
        admins_group.permissions.set(admins_permission)
    except Exception as e:
        print(f"An error occurred while creating groups and permissions: {e}")

    print("Groups and Permissions created successfully")






 