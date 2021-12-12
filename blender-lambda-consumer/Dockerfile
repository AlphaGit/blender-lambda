FROM public.ecr.aws/lambda/python:3.8

COPY *.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt .
RUN chmod 755 $(find . -type d)
RUN chmod 644 $(find . -type f)
RUN pip3 install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

CMD [ "consumer_function.handler" ]