FROM node:10 AS build_vue
WORKDIR  /dso

COPY /dso/package*.json ./
RUN npm install

COPY /dso ./
RUN npm run build


FROM nginx:alpine AS server
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build_vue /dso/dist ./
ENTRYPOINT ["nginx", "-g", "daemon off;"]