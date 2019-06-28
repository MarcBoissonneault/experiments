FROM python:3.7 as base

ARG PYPI_ACCESS_KEY
ARG PYPI_SECRET_KEY

# We install poetry system wide below, to make it accessible to further steps we need to add it to the PATH
# Sadly, Variables expansion is done prior to the build, wich means that doing so "ENV PATH "$HOME/something"
# will result in PATh = "something" since the "HOME" variable that represent the home of the current user
# is expanded before the actual user start to build.
# That's why we hard-coded the HOME to "/root" here
ENV HOME /root
ENV PATH $HOME/.poetry/bin:$PATH

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV POETRY_VERSION "0.12.16"

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y -q \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local
COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir pip -U && \
    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python - --version $POETRY_VERSION && \
    poetry config settings.virtualenvs.create false && \
    poetry install --no-dev


##########
# Dev
##########
FROM base as dev

RUN poetry install

WORKDIR /lib
COPY . .


##########
# Quality Checks
##########
FROM dev as checks

RUN isort -rc
RUN black --diff /lib
RUN mypy .
RUN pylama .
RUN poetry show -o


##########
# Release
##########
FROM base as release

ARG IMAGE_TAG
ENV IMAGE_TAG ${IMAGE_TAG:-latest}

ARG REVISION
ENV REVISION=${REVISION}

ARG VERSION
ENV VERSION=${VERSION}

ARG CI_BUILD_NUMBER
ENV CI_BUILD_NUMBER=${CI_BUILD_NUMBER}

ARG CI_BUILD_HOST
ENV CI_BUILD_HOST=${CI_BUILD_HOST}

ARG CI_BUILD_TIME
ENV CI_BUILD_TIME=${CI_BUILD_TIME}

WORKDIR /lib
COPY . .
