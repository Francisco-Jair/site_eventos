from django.core.mail import send_mail

def sendEmail(usuario):
    subject = "Assunto"
    message = "msg aqui"
    from_email = [usuario.email]
    send_mail(subject, message, "admin@gmail.com", from_email)

    