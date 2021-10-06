FROM nginx
ARG CONTAINERS_HOST=172.17.0.1
COPY nginx.conf.template /etc/nginx/conf.d/default.conf.template
RUN envsubst '${CONTAINERS_HOST}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]