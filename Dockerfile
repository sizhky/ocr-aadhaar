FROM continuumio/miniconda3
RUN apt update
RUN apt install -y tesseract-ocr
RUN apt install -y wget
# RUN mkdir -p ~/miniconda3
# RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
# RUN bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
# RUN rm -rf ~/miniconda3/miniconda.sh
# RUN ~/miniconda3/bin/conda init bash
# RUN ~/miniconda3/bin/conda init zsh
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY src /src
COPY static /static
COPY files /files
COPY templates /templates
COPY main.py main.py
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]