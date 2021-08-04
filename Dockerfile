FROM python:3.9-slim-buster as main
# Create new user appuser
RUN useradd --create-home appuser
USER appuser

RUN pip install --user -U \
    pip \
    setuptools \
    wheel

# Add new path to the binary files
ENV PATH="/home/appuser/.local/bin:${PATH}"

WORKDIR /home/appuser/app

# Install requirements
COPY --chown=appuser:appuser ./requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy source code as a new user
COPY --chown=appuser:appuser ./setup.py .
COPY --chown=appuser:appuser ./src ./src

# Install source code as a python package
RUN pip install --user -e .

EXPOSE 8080

# Run starting script
CMD ["scherunner"]
