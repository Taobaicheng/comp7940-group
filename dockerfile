FROM python
WORKDIR /chatbot
COPY . /chatbot
RUN pip install update
RUN pip install -r requirements.txt

ENV TLG_ACCESS_TOKEN=7389327487:AAEEnsk1JMj8fan1bUFSPV30nQ4_gtfBuxA
ENV BASICUREL=https://genai.hkbu.edu.hk/general/rest
ENV MODELNAME=gpt-4-o-mini
ENV APIVERSION=2024-05-01-preview
ENV GPT_ACCESSTOKEN=1de3005e-32a5-4438-84d1-13759a010d6f

CMD python chatbot.py