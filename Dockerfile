FROM python:3.11-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libasound2 \
    libxtst6 \
    libxdamage1 \
    libx11-xcb1 \
    libxfixes3 \
    libdrm2 \
    libxkbcommon0 \
    xdg-utils \
    wget \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libcairo-gobject2 \
    tzdata \
    curl \
    tar \
    chromium \
    chromium-driver \
    && apt-get clean

# Install Playwright
RUN pip install --no-cache-dir playwright

# Install OpenJDK from Adoptium
RUN mkdir -p /usr/share/man/man1 && \
    wget -qO- https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.16.1+1/OpenJDK11U-jre_x64_linux_hotspot_11.0.16.1_1.tar.gz | tar xz -C /opt && \
    ln -s /opt/jdk-11.0.16.1+1-jre/bin/java /usr/bin/java

# Install Allure
RUN curl -o allure-2.13.8.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz && \
    tar -zxvf allure-2.13.8.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
    rm allure-2.13.8.tgz

# Set the working directory
WORKDIR /usr/workspace

COPY requirements.txt /usr/workspace/
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir pytest
RUN playwright install chromium
