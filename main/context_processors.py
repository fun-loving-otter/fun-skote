from main.models import UserThrottledActionEntry


# TODO: write tests for this
def credits_usage(request):
    user = request.user

    if not user.is_authenticated:
        return {}

    usage = UserThrottledActionEntry.get_mapped_usage(user, user.subscription)
    return {
        'CREDITS_USAGE': usage
    }
