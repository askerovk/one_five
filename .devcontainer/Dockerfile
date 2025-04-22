FROM debian:12-slim

RUN apt update && apt install -y libgl1-mesa-glx libegl1-mesa \
    libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 \
    libxi6 libxtst6 -y

WORKDIR /usr/local/one_five_project

ENV CONDA_DIR=/opt/conda

RUN apt install wget -y

RUN wget -O /usr/local/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py312_25.1.1-2-Linux-x86_64.sh 

RUN bash /usr/local/miniconda.sh -b -p /opt/conda

ENV PATH="$PATH:/opt/conda/bin"

RUN conda create --name one_five -y python=3.12 pandas sqlalchemy psycopg2 nltk

# RUN pip install --upgrade pip

# ENV PYTHONUNBUFFERED 1

# WORKDIR /usr/local

# COPY requirements.txt ./requirements.txt
# RUN pip install -r requirements.txt

# COPY data ./data
# COPY src ./src

# COPY docker ./docker
# RUN chmod +x ./docker/entrypoint.sh
# ENTRYPOINT ["./docker/entrypoint.sh"]
