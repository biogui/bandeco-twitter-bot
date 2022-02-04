FROM python:3.8.3-alpine

RUN pip install --upgrade pip

RUN adduser -D bio
USER bio
WORKDIR /home/bio/

ENV PATH="/home/bio/.local/bin:${PATH}"

COPY --chown=bio:bio requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

COPY --chown=bio:bio src/main.py src/
COPY --chown=bio:bio src/api_control.py src/
COPY --chown=bio:bio src/menu_control.py src/

CMD ["python3", "src/main.py"]