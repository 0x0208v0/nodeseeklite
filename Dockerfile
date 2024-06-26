FROM python:3.11.9-slim-bookworm as pyhton311
WORKDIR /nodeseeklite_data
COPY ./src /nodeseeklite_data/src
COPY ./pyproject.toml /nodeseeklite_data/pyproject.toml
RUN  python -m pip install --upgrade build  && python -m build


FROM python:3.11.9-slim-bookworm


RUN apt update \
    && apt install --no-install-recommends -y vim \
    && apt install --no-install-recommends -y procps  \
    && apt install --no-install-recommends -y iputils-ping \
    && apt install --no-install-recommends -y net-tools \
    && apt install --no-install-recommends -y telnet \
    && apt install --no-install-recommends -y htop  \
    && apt install --no-install-recommends -y curl  \
    && apt install --no-install-recommends -y zip  \
    && apt install --no-install-recommends -y unzip \
    && echo done

WORKDIR /nodeseeklite_data

COPY --from=pyhton311 /nodeseeklite_data/dist /nodeseeklite_data/dist

RUN python -m pip install --no-cache-dir /nodeseeklite_data/dist/*.whl && rm -rf /nodeseeklite_data/dist


# docker build -f Dockerfile -t nodeseeklite .

# docker run --rm -it nodeseeklite bash
