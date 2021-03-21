FROM ethereum/client-go:alltools-v1.10.1

ENV HOME "/root"
WORKDIR "${HOME}"
COPY ./scripts ./scripts
RUN chmod -R +x "${HOME}/scripts"
ENV PATH "${PATH}:${HOME}/scripts"
