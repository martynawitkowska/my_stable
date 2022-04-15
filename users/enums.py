class UserType:
    NOT_KNOWN = 0
    VETERINARIAN = 1
    FARRIER = 2
    STABLE_OWNER = 3

    CHOICES = (
        (NOT_KNOWN, 'Choose occupation'),
        (VETERINARIAN, 'Vet'),
        (FARRIER, 'Farrier'),
        (STABLE_OWNER, 'Stable owner'),
    )
