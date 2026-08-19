# ── Stage 1: Dependencies & Build ─────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build SvelteKit application
RUN npm run build || true

# ── Stage 2: Runtime ──────────────────────────────────────────
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Install production dependencies
COPY package*.json ./
RUN npm ci --omit=dev || npm ci

# Copy built application and source
COPY --from=builder /app ./

EXPOSE 5173

# Run Vite dev / preview server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
