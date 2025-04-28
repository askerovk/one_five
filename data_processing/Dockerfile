FROM debian:12-slim

RUN apt update && apt install -y libgl1-mesa-glx libegl1-mesa \
    libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 \
    libxi6 libxtst6 -y

RUN mkdir /usr/local/one_five_project

WORKDIR /usr/local/one_five_project

ENV CONDA_DIR=/opt/conda

RUN apt install wget -y

RUN wget -O /usr/local/miniconda.sh \
    https://repo.anaconda.com/miniconda/Miniconda3-py312_25.1.1-2-Linux-x86_64.sh 

RUN bash /usr/local/miniconda.sh -b -p /opt/conda

ENV PATH="$PATH:/opt/conda/bin"

RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict

COPY . .

RUN conda create --name one_five -y python=3.12 pandas sqlalchemy \
    nltk clickhouse-connect

SHELL ["conda", "run", "-n", "one_five", "/bin/bash", "-c"]

RUN python -c "import nltk; nltk.download(['punkt_tab', 'stopwords'])"

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "one_five", "python", "src/app.py"]