FROM python:3.11-slim
WORKDIR /agent
COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt
COPY agent.py .
CMD ["python","agent.py"]
