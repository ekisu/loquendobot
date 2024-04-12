FROM alpine:3.18 AS download-ffmpeg

WORKDIR /ffmpeg-files
RUN apk add --no-cache xz curl && \
    curl -O https://www.johnvansickle.com/ffmpeg/old-releases/ffmpeg-6.0.1-amd64-static.tar.xz && \
    tar xvf ffmpeg-6.0.1-amd64-static.tar.xz --strip-components=1 && \
    rm ffmpeg-6.0.1-amd64-static.tar.xz

FROM alpine:3.18 AS generate-requirements

# Copy poetry lock files
COPY poetry.lock ${LAMBDA_TASK_ROOT}
COPY pyproject.toml ${LAMBDA_TASK_ROOT}

RUN apk add --no-cache poetry && \
    poetry export --without-hashes -f requirements.txt -o requirements.txt

FROM public.ecr.aws/lambda/python:3.12

# Install ffmpeg and poetry
COPY --from=download-ffmpeg /ffmpeg-files/* /usr/local/bin
COPY --from=generate-requirements requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "loquendobot.main.lambda_handler" ]
