#!/usr/bin/env bash
# Script to prepare web servers for deployment of web_static

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get install -y nginx

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
    </head>
      <body>
          Holberton School
	    </body>
	    </html>" | sudo tee /data/web_static/releases/test/index.html

	    # Create a symbolic link
	    sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

	    # Give ownership to the ubuntu user and group
	    sudo chown -R ubuntu:ubuntu /data/

	    # Update Nginx configuration
	    sudo sed -i '/listen 80 default_server;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

	    # Restart Nginx
	    sudo service nginx restart

	    # Exit successfully
	    exit 0
