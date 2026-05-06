# Stage 1: Build stage
FROM node:20-alpine as build-stage

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps

# Copy project files
COPY . .

# Build the app
RUN npm run build

# Stage 2: Production stage
FROM nginx:stable-alpine as production-stage

# Copy build artifacts to nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy nginx configuration
# We'll provide a specific nginx config for the frontend if needed, 
# but usually, we serve it via the main nginx proxy.
# For now, just the default is fine if this container is used standalone.

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
