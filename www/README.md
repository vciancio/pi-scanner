# WWW Server Setup

> Note: Because we have to use Google OAuth to access the Google-Photos API, it gets a bit tricky to fetch the token for a non-public ip. Google does not allow local ips as a redirect_uri. To get around this, we will be using [sslip.io](sslip.io), which is a DNS service that forwards requests to an ip that's provided.

## Flask

First thing to do is setup flask. We'll be running it via localhost as Nginx will handle the routing for us.

~~~ bash
(cd www && python -m venv www-env && pip3 install -r requirements.txt)
~~~

## SSL

This is needed for Google OAuth.

Generate your certificates form the repo dir:
~~~bash
mkdir www/ssl
sudo openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout www/ssl/privkey.pem -out www/ssl/fullchain.pem
~~~

## Nginx

Install Nginx from apt.

~~~bash
sudo apt-get install nginx
~~~

Update the config at `www/nginx.config` by replacing updating the following lines in the config file with the path to your local copy of the repo.

~~~
ssl_certificate     /home/pi/pi-scanner/www/ssl/fullchain.pem;
ssl_certificate_key /home/pi/pi-scanner/www/ssl/privkey.pem;
~~~

Then copy the nginx config over and restart nginx to apply changes.

~~~bash
sudo cp www/nginx.conf /etc/nginx/sites-enabled/pi-scanner.conf
sudo nginx -t # Tests Nginx Config
sudo service nginx restart
~~~

Test your Nginx Config & Flask setup by going to the following:

~~~bash
source www/www-env/bin/activate
python -m www

# Access http://YOUR_LOCAL_IP to see if you can see the web page.
~~~

## Google Photos OAuth

1. Create a new project in the [Google Cloud Console](https://console.cloud.google.com/apis/dashboard).
2. Go to the [Credentials page](https://console.cloud.google.com/apis/credentials) for your app.
3. Create a new OAuth 2.0 Client ID
    * Set the application type as `Web application`.
    * Add an authorized redirect URI and make it `YOUR_LOCAL_IP.sslip.io/auth/google-photos`.
4. Hit _Create_.
5. A dialog box containing your client secret and client id should appear. Add the following to your `.env` folder in the root of the project:

~~~
GOOGLE_PHOTOS_CLIENT_SECRET=your_client_secret
GOOGLE_PHOTOS_CLIENT_ID=your_client_id
~~~