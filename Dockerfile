FROM python:3.10

# Update apt
RUN apt-get update

# Installing python3-dev header for datrie library
#RUN apt-get install -y python3-dev
RUN apt-get update && apt-get install -y python3-dev

# Install python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN pip install python-terrier

# Install Javac
RUN apt-get install -y openjdk-17-jdk-headless

# Install Ollama
#RUN curl -fsSL https://ollama.com/install.sh | sh

# Set workspace in container
WORKDIR /workspace

# Copy Project into container
COPY . /workspace/

# Change directory and make trec_eval executable
WORKDIR /workspace/trec_eval-9.0.7
RUN make

# Return in work directory
WORKDIR /workspace


#Set Path variables for trec_eval and the SIMIIR project
#RUN export PYTHONPATH="${PYTHONPATH}:/workspace/ifind:/workspace/simiir"
#RUN export PATH="/workspace/trec_eval-9.0.7:$PATH"
ENV PYTHONPATH="/workspace/ifind:/workspace/simiir:${PYTHONPATH}"
ENV PATH="/workspace/trec_eval-9.0.7:$PATH"

# Keep the container running
ENTRYPOINT ["tail", "-f", "/dev/null"]
