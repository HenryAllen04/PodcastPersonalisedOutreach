# Purpose: Docker container for PODVOX React frontend with development and production modes

# Development stage
FROM node:20-alpine AS development

# Set working directory
WORKDIR /app

# Install dependencies first for better caching
COPY package.json package-lock.json* ./
RUN npm install

# Copy source code
COPY . .

# Expose the port
EXPOSE 3000

# Start the development server with proper host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]

# Build stage for production
FROM node:20-alpine AS build
WORKDIR /frontend
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build

# Production stage with Nginx
FROM nginx:alpine AS production
COPY --from=build /frontend/dist /usr/share/nginx/html
EXPOSE 3000

# Custom nginx config to serve on port 3000
RUN echo 'server { listen 3000; location / { root /usr/share/nginx/html; index index.html; try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"] 