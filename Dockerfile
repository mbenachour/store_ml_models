FROM python:2.7.15-stretch
COPY server.py .
RUN python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose awscli boto3
RUN python -m pip install -U scikit-learn
EXPOSE 8088
CMD python server.py
