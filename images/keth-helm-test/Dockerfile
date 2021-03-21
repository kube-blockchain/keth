FROM ethereum/client-go:alltools-v1.10.1

RUN apk add curl
ENV HOME "/root"
ENV PATH "${PATH}:${HOME}/scripts"

WORKDIR "${HOME}"
COPY ./scripts ./scripts
RUN chmod -R +x "${HOME}/scripts"
