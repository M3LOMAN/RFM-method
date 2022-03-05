FROM python

RUN python -m pip install matplotlib pandas seaborn

WORKDIR /C:/Users/Владимир/OneDrive/Документы/rfm

COPY . .

ENTRYPOINT ["python"]

CMD ["rfm.py"]