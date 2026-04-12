FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Move into the app folder FIRST
WORKDIR /app

# Now copy the files into /app
COPY ./pyproject.toml ./
COPY ./README.md ./
COPY ./app ./app

# Run the install safely inside /app
RUN pip install .

ENTRYPOINT ["python"]

CMD ["-m", "app.main"]