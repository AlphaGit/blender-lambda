FROM nytimes/blender:3.1-cpu-ubuntu18.04

ARG FUNCTION_DIR="/home/app"
RUN mkdir -p $FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}

RUN pip install boto3
RUN pip install awslambdaric --target ${FUNCTION_DIR}

ENTRYPOINT [ "/bin/3.1/python/bin/python3.10", "-m", "awslambdaric" ]
CMD [ "producer_function.handler" ]

COPY *.py ${FUNCTION_DIR}/
RUN chmod 755 $(find . -type d) && \
    chmod 644 $(find . -type f)