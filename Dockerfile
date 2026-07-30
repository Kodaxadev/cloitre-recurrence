# Pinned reproduction environment for the Cloitre recurrence research package.
#
# CI runs on `ubuntu-latest` and `windows-latest`, which are moving targets. This
# image pins every toolchain to the exact version the committed results were
# produced with, so a reviewer can reproduce them years from now:
#
#   Python 3.13   (base image)
#   Rust   1.94.0 (matches .github/workflows/ci.yml)
#   Lean   4.32.2 (matches lean-toolchain)
#
# Build and run the full check suite:
#
#   docker build -t cloitre .
#   docker run --rm cloitre
#
# Drop into a shell instead:
#
#   docker run --rm -it cloitre bash
#
# The image deliberately installs no Rust or Python packages beyond the
# toolchains: both frameworks have zero third-party dependencies by design.

FROM python:3.13-slim-bookworm

# `curl` and `ca-certificates` are needed only to fetch the pinned toolchains;
# `git` is needed by lake, and `build-essential` supplies the linker for cargo.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

ENV RUSTUP_HOME=/opt/rustup \
    CARGO_HOME=/opt/cargo \
    ELAN_HOME=/opt/elan
ENV PATH=/opt/cargo/bin:/opt/elan/bin:$PATH

# Rust, pinned to the CI toolchain.
ARG RUST_VERSION=1.94.0
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
      | sh -s -- -y --no-modify-path --profile minimal \
        --default-toolchain "${RUST_VERSION}" \
    && rustc --version \
    && cargo --version

# Lean, pinned by lean-toolchain rather than by a literal here, so the image and
# the repository cannot drift apart.
COPY lean-toolchain /tmp/lean-toolchain
RUN curl --proto '=https' --tlsv1.2 -sSf \
      https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
      | sh -s -- -y --no-modify-path \
        --default-toolchain "$(cut -d: -f2 /tmp/lean-toolchain)" \
    && lean --version \
    && lake --version

WORKDIR /work
COPY . /work

# `reproduce.sh` runs exactly what CI runs, in the same order.
CMD ["bash", "scripts/reproduce.sh"]
