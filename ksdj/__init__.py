"""
    KSDJ - Django interface for Kickstart server using NFS & PXE.
    By: nullpass
    Running:  python 3.4.1 && django 1.7c2+

Bugs:
    5.5 doesn't know what '%end' is, 5.10 probably does, 6+ certainly does; have to strip it out before .write()
    email addresses of corporate length probably won't fit- same issue everyone else ran into and is why there are
        so many auth extentions for Dj. Writing my own fix, importing someone elses, or going pure LDAP are all about
        the same about of work so I'm going to go for ldap next chance I get.
            ...that is- if I can get the py3 branch to actually compile...
    Editing a client will overwrite any customizations done to its kickstart file.

Really sick of screwing up plural/non-plural names. I know where it makes sense to add an 's', but I burned so much typo/recompile time in the past
I'm just going to make everything singular going forward.


TODO:
    
    

recent:
    This app is done enough for what I need, no more work on it for now.
    named for an old url in another project, this is the start of my logging system.
    I looked at some existing options on the webernets but as happens far too often I found none of them fit the bill.
    Started off with log_form_valid which hits after form validation but before DB writing.
    Writting all of POST to the database is overkill for most cases, but kickstart is such a sensitive system (especially given this web interface
    is so new) I want to be able to track all changes to the max.
    

Files we modify: 

ks/etc/hosts
ks/etc/hosts.allow
ks/etc/pxe_clients.conf
ks/etc/ks.d/{hostname}.ks
ks/etc/clients.d/{hostname}.sh
    CLIENT_HOSTNAME="
    CLIENT_MAC="
    CLIENT_IPADDR="
    CLIENT_NETMASK="
    CLIENT_GATEWAY="
    CLIENT_TYPE="
    CLIENT_OS="
    SERVER_IPADDR="
tftp/01-{mac address}

ks/etc/dhcpd.conf
ks/etc/vlan_XX.conf


-==-

If I get hit by a bus here are the non-prod deployment notes; of course you don't need to worry about any of this in prod.

VIRTUALENV:
    get the latest from their github repo. v1.9.x doesn't work with py3.4, latest does.

NGINX:
    -1.7.4 works ok
    ./configure --without-http_rewrite_module --with-http_ssl_module --with-debug && make && make install
    mkdir /usr/local/nginx/ssl/
    cd /usr/local/nginx/ssl/
    openssl genrsa -des3 -out server.key 1024
    openssl req -new -key server.key -out server.csr
    openssl rsa -in server.key.org -out server.key
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt


# ksdj_nginx.conf
user apache;
events {
    worker_connections  1024;
}
http {
    upstream django {
        server unix:///tmp/ksdj.socket;
    }
    server {
        listen              443 ssl;
        ssl_protocols       SSLv3 TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         HIGH:!aNULL:!MD5;
        ssl on;
        ssl_certificate /usr/local/nginx/ssl/server.crt;
        ssl_certificate_key /usr/local/nginx/ssl/server.key;
        server_name kickstart.example.tld;
        charset     utf-8;
        location /static/js/ {
            default_type text/javascript;
            alias /opt/www/ksdj/static/js/;
        }
        location /static/css/ {
            default_type text/css;
            alias /opt/www/ksdj/static/css/;
        }
        location /static/admin/js/ {
            default_type text/javascript;
            alias /opt/www/ksdj/static/static/admin/js/;
        }
        location /static/admin/css/ {
            default_type text/css;
            alias /opt/www/ksdj/static/static/admin/css/;
        }
        location / {
            uwsgi_pass  django;
            include     /usr/local/nginx/conf/uwsgi_params;
        }
    }
}

UWSGI
    -lts is fine
    cd /opt/www/
    source bin/activate
    cd ksdj/
    uwsgi -s /tmp/ksdj.socket --uid=apache --gid=apache --module ksdj.wsgi --chmod-socket=600 --enable-threads


"""
