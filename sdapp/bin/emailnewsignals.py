from django.core.mail import send_mail



def pwreminder(signals):
    if signals.count() = 1:
        subject = 'New Signal'
        message = 'We have detected a new signal for %s'
    else:
        subject = 'New Signal'
    new_pw = User.objects.make_random_password()

    message =\
        'We received your password reset request for [PRODUCT NAME].\n'\
        + 'Your new password is %s and we suggest that you reset this to '\
        % new_pw\
        + 'something easier to remember. If you did not request a '\
        + 'password reset, please contact us at [SUPPORT EMAIL ADDRESS].\n'\
        + 'If you have any questions, feel free to reply to this email.\n\n'\
        + 'Regards,\n'\
        + '[COMPANY NAME] Support'
    from_email = settings.EMAIL_HOST_USER
    request.user.email
    to_list = [request.user.email]

    u = User.objects.get(username__exact=request.user.username)
    u.set_password(new_pw)
    u.save()
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    print message
    request.user.email

    messagetext = \
        'You should receive a new temporary password shortly.'
    messages.warning(request, messagetext)
    return HttpResponseRedirect('/changepw/')