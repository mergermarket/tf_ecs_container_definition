FROM python:3-alpine
COPY requirements.txt .

ENV TERRAFORM_VERSION=0.11.15
ENV TERRAFORM_ZIP=terraform_${TERRAFORM_VERSION}_linux_amd64.zip
ENV TERRAFORM_SUM=e6c8c884de6c353cf98252c5e11faf972d4b30b5d070ab5ff70eaf92660a5aac

RUN apk add -U ca-certificates curl gcc musl-dev libffi-dev openssl-dev && \
    cd /tmp && \
    curl -fsSLO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/${TERRAFORM_ZIP} && \
    echo "${TERRAFORM_SUM}  /tmp/${TERRAFORM_ZIP}" | sha256sum -c - && \
    unzip /tmp/${TERRAFORM_ZIP} -d /usr/bin && \
    rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

RUN pip install --no-cache-dir -r requirements.txt
