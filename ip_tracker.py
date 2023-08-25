from flask import Flask, request, redirect

web_application = Flask(__name__)
link_website = "https://www.facebook.com/zeropraxen/?locale=de_DE"


@web_application.route('/')
def capture_ip_and_redirect():
    global link_website
    user_ip_address = request.remote_addr
    with open("ip_addresses.txt", "a") as file:
        file.write(user_ip_address)
    return redirect(link_website)
