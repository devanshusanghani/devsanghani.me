FROM python:3.12-alpine AS builder

# Install build dependencies and mkdocs-material with all plugins
RUN apk add --no-cache \
    git

# Clean up cache to reduce image size
WORKDIR /install

# Copy requirements files
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-alpine
WORKDIR /docs

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Install git for git-revision-date-localized-plugin
RUN apk add --no-cache git

# Create non-root user
RUN adduser -D mkdocs

# Create necessary directories with proper permissions
RUN mkdir -p /docs/.cache/plugins/rss && \
    mkdir -p /docs/.git && \
    chown -R mkdocs:mkdocs /docs

# Initialize git repository
RUN git init /docs

# Copy website content
COPY docs/ docs/
COPY mkdocs.yml ./
COPY theme/ theme/

# Set permissions
RUN chown -R mkdocs:mkdocs /docs && \
    git config --global --add safe.directory /docs

# Switch to non-root user
USER mkdocs

# Add files and create initial commit
RUN git add . && \
    git -c user.name="Docker" -c user.email="docker@local" commit -m "Initial commit"

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --spider -q http://localhost:8000 || exit 1

# Set entrypoint and default command
ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000", "--livereload"]