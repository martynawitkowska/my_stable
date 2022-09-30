class WeekDays:
    CHOOSE_DAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    CHOICES = (
        (CHOOSE_DAY, 'Choose a day'),
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )


class Meals:
    OPTION = 0
    BREAKFAST = 1
    DINNER = 2
    SUPPER = 3

    CHOICES = (
        (OPTION, 'Choose a meal'),
        (BREAKFAST, 'Breakfast'),
        (DINNER, 'Dinner'),
        (SUPPER, 'Supper'),
    )
