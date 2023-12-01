FROM python:3.11-slim

#ENV DOCKER_BUILDKIT 1
#ENV COMPOSE_DOCKER_CLI_BUILD 1
ENV PROJECT_DIR BrainMRI-images-classification-APIs

WORKDIR /${PROJECT_DIR}
ADD ./requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install apt-utils gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*  && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu

COPY ./src/ /${PROJECT_DIR}/src/
COPY ./models/ /${PROJECT_DIR}/models/
COPY ./sample_images/ /${PROJECT_DIR}/sample_images/

ENV MODEL_FILEPATH /${PROJECT_DIR}/models/efficientnet_v2_m-Fold-1.onnx
ENV LABEL_FILEPATH /${PROJECT_DIR}/models/label.json
ENV LOG_LEVEL DEBUG
ENV LOG_FORMAT TEXT

COPY ./run.sh /${PROJECT_DIR}/run.sh
RUN chmod +x /${PROJECT_DIR}/run.sh
#CMD ["./run.sh"]
