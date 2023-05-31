FROM python:3.11-alpine

RUN apk update
RUN apk upgrade --available && sync

# Required system packages.
RUN apk add --no-cache bash wget libc-dev ca-certificates gcc

# Download and set up the Rust environment.
# The default version available in the package manager contains several vulnerabilities!
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.68.1

RUN set -eux; \
    apkArch="$(apk --print-arch)"; \
    case "$apkArch" in \
        x86_64) rustArch='x86_64-unknown-linux-musl'; rustupSha256='241a99ff02accd2e8e0ef3a46aaa59f8d6934b1bb6e4fba158e1806ae028eb25' ;; \
        aarch64) rustArch='aarch64-unknown-linux-musl'; rustupSha256='6a2691ced61ef616ca196bab4b6ba7b0fc5a092923955106a0c8e0afa31dbce4' ;; \
        *) echo >&2 "unsupported architecture: $apkArch"; exit 1 ;; \
    esac; \
    url="https://static.rust-lang.org/rustup/archive/1.25.2/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --profile minimal --default-toolchain $RUST_VERSION --default-host ${rustArch}; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    rustup --version; \
    cargo --version; \
    rustc --version;

# Copy all necessary files.
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
COPY server_start.sh .

WORKDIR /app/src
COPY src/. .

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# Install Poetry and the packages specified in the toml.
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

EXPOSE 5002

# Run the Uvicorn server via the bash script 'server_start.sh'.
ENTRYPOINT ["bash", "server_start.sh"]
