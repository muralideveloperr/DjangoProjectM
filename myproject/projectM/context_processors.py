def global_page_title(request):
    path_title_map = {
        '/': 'Home PROJECT-M',
        '/about': 'About PROJECT-M',
        '/services': 'Services PROJECT-M',
        '/portfolio': 'Portfolio PROJECT-M',
        '/contact': 'Contact PROJECT-M',
        '/resume': 'Resume PROJECT-M',
        '/services/resume_builder/<slug:slug>': 'Resume Builder PROJECT-M',
        '/services/create_resume/<slug:slug>': 'Create Resume PROJECT-M'
    }

    current_path = request.path
    default_title = 'PROJECT-M'

    page_title = path_title_map.get(current_path, default_title)

    return {'page_title': page_title}

