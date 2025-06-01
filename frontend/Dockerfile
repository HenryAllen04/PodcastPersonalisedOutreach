# Purpose: Docker container for PODVOX React frontend with nginx serving

# Build stage
FROM node:20-alpine AS build
WORKDIR /frontend
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build

# Serve with Nginx
FROM nginx:alpine
COPY --from=build /frontend/dist /usr/share/nginx/html
EXPOSE 3000

# Custom nginx config to serve on port 3000
RUN echo 'server { listen 3000; location / { root /usr/share/nginx/html; index index.html; try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"] 