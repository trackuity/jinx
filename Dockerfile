FROM python:3.9.7-alpine as builder
RUN mkdir /jinx
COPY setup.py /jinx/
COPY jinx /jinx/jinx/
RUN \
    apk add db-dev build-base; \
    cd /jinx; \
    python -m venv venv; \
    LDFLAGS="-L/usr/lib/" CFLAGS="-I/usr/include" venv/bin/pip install \
        -e . \
        --extra-index-url=https://alpine-wheels.github.io/index/

FROM python:3.9.7-alpine
ENV JINX_DATA_DIR=/var/jinx
ENV JINX_PORT=8000
ENV JINX_HOST=0.0.0.0
COPY --from=builder /jinx /jinx
RUN apk add db; ln -s /jinx/venv/bin/jinx /usr/bin/jinx
EXPOSE 8000
WORKDIR /jinx
CMD jinx serve -h $JINX_HOST -p $JINX_PORT -d $JINX_DATA_DIR
