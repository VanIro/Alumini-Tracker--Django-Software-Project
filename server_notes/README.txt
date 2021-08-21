
DO NOT TOUCH THE SERVER UNLESS YOU COMPLETELY KNOW WHAT YOU ARE DOING
THERE ARE MULTIPLE PROJECTS HOSTED THERE AND THEY SHOULD NOT BE DOWN IN ANY CIRCUMSTANCE.

THE ONLY FILES YOU WILL NEED TO TOUCH ARE IN /home/bob/DoeceAlumniStudentPortal/

The unedited server notes(as I took them) are in monolith_server_notes.txt
Consult that if you can't find what you are looking for in any of the other files.

The server is running CentOS
First the traffic goes to a httpd(Apache server)(httpd_settings.txt has a working config. However, there may be newer changes, which you CANNOT remove)
I have redirected most of the traffic from there(except a few legacy applications) to nginx
nginx(nginx_settings.txt) and gunicorn(gunicorn_settings.txt) together serve the django application.
