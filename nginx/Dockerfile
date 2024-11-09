FROM nginx:latest

COPY ./forkapi/nginx.conf /etc/nginx/nginx.conf
COPY ./forkapi/forkapi.nginx.conf /etc/nginx/sites-available/
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/forkapi.nginx.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
