import datetime
p_name = "محسن علی زاده"
d_name = 'مریم مینایی'
timee = datetime.datetime.now()
pation_msg = f"امروز با دکتر با نام {d_name} درزمان {timee} ملاقات دارد"
doctor_msg = f"در ساعت {timee} با مریض بنام {p_name} ملاقات"

# Make sure to encode the messages using UTF-8
pation_msg = pation_msg.encode('utf-8')
doctor_msg = doctor_msg.encode('utf-8')

