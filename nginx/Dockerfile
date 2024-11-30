FROM nginx:latest

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/forkapi.nginx.template /etc/nginx/sites-available/
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/forkapi.nginx.template /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
