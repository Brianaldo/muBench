from python:3.8.16-slim-buster

RUN apt update
RUN apt install -y gpg ca-certificates curl bash-completion apt-transport-https vim nano iproute2 iputils-ping apache2-utils --no-install-recommends

# kubectl
RUN mkdir /etc/apt/keyrings
RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
RUN echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list
RUN apt update
RUN apt install -y kubectl --no-install-recommends
RUN mkdir /root/.kube

# kubectl autocomplete
RUN echo "source /usr/share/bash-completion/bash_completion" >> .bashrc
RUN echo 'source <(kubectl completion bash)' >>~/.bashrc
RUN echo 'alias k=kubectl' >>~/.bashrc
RUN echo 'complete -o default -F __start_kubectl k' >>~/.bashrc

# heml
RUN curl https://baltocdn.com/helm/signing.asc | gpg --dearmor > /usr/share/keyrings/helm.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" > /etc/apt/sources.list.d/helm-stable-debian.list
RUN apt update
RUN apt install -y helm

# welcome message
COPY welcome.sh /etc/profile.d
RUN chmod a+rx /etc/profile.d/welcome.sh
RUN echo "/etc/profile.d/welcome.sh" >> /root/.bashrc

# muBench software
RUN apt install -y git libpangocairo-1.0-0 --no-install-recommends
COPY . /root/muBench
RUN pip3 install -r /root/muBench/requirements.txt

WORKDIR /root/muBench

CMD [ "sleep", "infinity"]
