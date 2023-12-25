import krpc
conn = krpc.connect(name='Status Check')
print(conn.krpc.get_status().version)
print('Соединение установлено\nРакета готова к запуску')