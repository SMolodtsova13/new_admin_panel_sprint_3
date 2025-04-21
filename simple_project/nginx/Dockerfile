FROM nginx:latest

RUN rm /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh

CMD ["nginx", "-g", "daemon off;"]
