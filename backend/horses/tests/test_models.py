from horses.models import Horse, Stable


def test_add_horse(horse):
    horses = Horse.objects.all()
    assert len(horses) == 1


def test_add_stable(stable):
    stables = Stable.objects.all()
    assert len(stables) == 1
