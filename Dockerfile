# First stage: Build environment with all dependencies
FROM python:3.11-alpine AS builder

WORKDIR /build
COPY Pipfile Pipfile.lock /build/


RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Second stage: Setup the runtime environment
FROM python:3.11-alpine

WORKDIR /oxygen-cs-grp01-eq6

COPY --from=builder /build/Pipfile /build/Pipfile.lock /oxygen-cs-grp01-eq6/
COPY --from=builder /root/.local/share/virtualenvs /root/.local/share/virtualenvs

COPY src /oxygen-cs-grp01-eq6/src

ENV PYTHONUNBUFFERED=1

CMD ["pipenv", "run", "start"]
