FROM python:3.9.16

ARG PYPI_USERNAME
ENV PYPI_USERNAME=$PYPI_USERNAME

ARG PYPI_PASSWORD
ENV PYPI_PASSWORD=$PYPI_PASSWORD

# installing poetry
ENV POETRY_HOME=/etc/poetry \
    POETRY_VERSION=1.3.1
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update && \
    apt-get install -y -q build-essential curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 -

# copying package files
COPY . ./

# publishing package
RUN poetry build

# for test PyPI index (local development)
#RUN poetry config repositories.testpypi https://test.pypi.org/legacy/
#RUN poetry publish --repository testpypi --username $PYPI_USERNAME --password $PYPI_PASSWORD

# for real PyPI index
RUN poetry publish --username $PYPI_USERNAME --password $PYPI_PASSWORD
