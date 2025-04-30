FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxrandr2 \
    libxcursor1 \
    libxfixes3 \
    libxi6 \
    libxtst6 \
    libxss1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libice6 \
    && rm -rf /var/lib/apt/lists/*
    
COPY  requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN echo "alias normi='flake8'" >> ~/.bashrc

CMD [ "bash" ]