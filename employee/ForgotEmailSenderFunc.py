from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def sendPasswordResetEmail(current_user, domain_name):
    userid_encode = urlsafe_base64_encode(force_bytes(current_user.pk))
    token = default_token_generator.make_token(current_user)
    url = f'{domain_name}/reset-password/{userid_encode}/{token}'
    html_content = f'''
                  <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 0;
                                    padding: 0;
                                    background-color: #f5f5f5;
                                }}
                                .container {{
                                
                                    padding: 20px;
                                    background-color: #ffffff;
                                    border-radius: 10px;
                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                }}
                                h3 {{
                                    color: #333333;
                                }}
                                p {{
                                    color: #666666;
                                }}
                                a {{
                                    display: inline-block;
                                    padding: 10px 20px;
                                    background-color: #007bff;
                                    color: #ffffff;
                                    text-decoration: none;
                                    border-radius: 5px;
                                }}
                                a:hover {{
                                    background-color: #0056b3;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <h3>Hello {current_user.name},</h3>
                                <p>Please click on the below to Reset your password</p>
                                <p><a href="{url}" style="color: #ffffff;">Reset Password</a></p>
                                <p>Thanks & Regards,</p>
                                <p>Employee Support</p>
                                <p>Simply 2 Cloud</p>
                            </div>
                        </body>
                        </html>
    '''
    email_sender = EmailMultiAlternatives("Attendence App Forgot Password", "", 'otp@simply2cloud.com', [current_user.email, 'bahimunna457@gmail.com'])
    email_sender.attach_alternative(html_content, "text/html")
    email_sender.send()