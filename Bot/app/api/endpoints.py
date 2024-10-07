class AdminEndpoints:
    pass


class UserEndpoints:
    # Activity
    get_activities = '/activity/all'
    get_activity_by_name = '/activity/by_name?name={name}'

    # School
    get_class_by_number = '/class/{class_number}'

    get_elementary_classes = '/class/elementary'
    get_middle_classes = '/class/middle'
    get_high_classes = '/class/high'

    # Teacher
    get_teacher_by_class = '/teacher/{class_number}'
    get_all_teachers = '/teacher/all/teachers'
