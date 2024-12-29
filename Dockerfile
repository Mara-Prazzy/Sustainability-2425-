# Use the AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.9

# Copy application files to the container
COPY kaatru_ws-data.py ${LAMBDA_TASK_ROOT}/
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Install dependencies
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Command to run the Lambda function handler
CMD ["kaatru_ws-data.lambda_handler"]
