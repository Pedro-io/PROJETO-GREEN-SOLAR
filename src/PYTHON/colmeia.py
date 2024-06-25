import datetime, time, csv, os, sys, tempfile
from datetime import datetime, timedelta
from pycampbellcr1000 import CR1000

recordFile = '/testfolder/colmeia/lastInsert'
csvFile = '/testfolder/colmeia/colmeia.csv'
minutesDelta = timedelta(minutes = 2880)
idleTime = 90
tmpFilled = False
index = 0

def emergencyHalt(b):
	if b == True:
		with open(tmp.name, 'rb') as tmpfile:
			errorLastInsert = tmpfile.read()
			with open('ARQUIVO DE ERRO.txt','w') as ef:
				ef.write('Ultima aquisicao de dados: \n\n', errorLastInsert)
	print '\n\nERRO FATAL. INTERROMPENDO O PROGRAMA.'
	sys.exit()

def getLastRecord():
	try:	
		with open(recordFile, 'rb') as file:
			if (os.stat(recordFile).st_size == 0):
				print '\nUltimo registro nulo.'
				emergencyHalt(tmpFilled)
			else:
				textData = file.read()
				localLastInsert = datetime.strptime(textData, '%Y-%m-%d %H:%M:%S')
	except Exception, e:
		localLastInsert = -1
		print '\nExcecao 01: ', e
	return localLastInsert

def getCampbellData(localLastInsert):
	print 'Iniciando coleta de dados ...'
	start = localLastInsert
	stop = start + minutesDelta
	try:
		print 'Estabelecendo comunicacao com o Campbell CR1000 ...'
		device = CR1000.from_url('serial:/dev/ttyUSB0:38400')
		print 'Conexao estabelecida'
		print 'Buscando dados ...'
		localData = device.get_data('colmeia',start,stop)
		dataSize = len(localData) - 1
		while dataSize == 0:
			start = stop
			stop += minutesDelta
			localData = device.get_data('colmeia',start,stop)
			dataSize = len(localData) - 1
		print 'Dados adquiridos: ', dataSize, '\n'
	except Exception, e:
		localData = -1
		print '\nExcecao 02: ', e
	return localData

def getCurrentIndex(localLastInsert, localData):
	indexLocal = 0
	x = indexLocal
	while x <= (len(localData) - 1):
		if localLastInsert == data[x]['Datetime']:
			indexLocal = 0
			break
		x += 1
	if indexLocal != (len(localData) - 1):
		indexLocal += 1
	else:
		indexLocal = -1
	return indexLocal

def storeCsvData(localIndex, localData):
	x = localIndex
	print 'Iniciando registro de dados ...'
	while x <= (len(localData) - 1):
		try:
			pointData = {
			'Datetime':localData[x]['Datetime'],
			'RecNbr':localData[x]['RecNbr'],
			'Temperatura':localData[x]['Temperatura'],
			'Velocidade_do_vento':localData[x]['Velocidade_do_vento'],
			'Umidade':localData[x]['Umidade'],
			'Direcao_do_vento':localData[x]['Direcao_do_vento'],
			'Pressao_do_ar':localData[x]['Pressao_do_ar'],
			'BattV':localData[x]['BattV'],
			'Precipitacao':localData[x]['Precipitacao'],
			'PTemp_C':localData[x]['PTemp_C']
			}
			
			#print '\n',pointData,'\n'
			
			dateValue = pointData['Datetime']
			csvFile = dbcheck.getFilePath(dateValue)

			with open(csvFile, 'ab+') as file:
				writer = csv.DictWriter(file, pointData.keys())
				if (os.stat(csvFile).st_size == 0):
					writer.writeheader()
				writer.writerow(pointData)
			localTmpFilled = setNewLastRecord(dateValue)
			print '\nArquivo armazenado: \n'
			print pointData

		except Exception, e:
			print '\nErro no processo de armazenamento.'
			print 'Excecao 03: ', e
		x += 1
	print '\nArmazenamento de dados concluido'	
	return localTmpFilled

def setNewLastRecord(newLastInsert):
	newLastInsert = str(newLastInsert)
	try:
		with open(tmp.name, 'w') as tmpfile:
			tmpfile.write(newLastInsert)
			tmpStatus = True
		with open(recordFile, 'w') as file:
			textNum = file.write(newLastInsert)
	except Exception, e:
		textNum = -1
		print 'Excecao 04: ', e
	if textNum == -1:
		emergencyHalt(tmpFilled)
	return tmpStatus

while True:
	tmpFilled = False
	with tempfile.NamedTemporaryFile() as tmp:
		print '\nLoop Iniciado\n'
		lastInsert = getLastRecord()
		if lastInsert != -1:
			data = getCampbellData(lastInsert)
			if data != -1:
				index = getCurrentIndex(lastInsert,data)
				if index != -1:
					tmpFilled = storeCsvData(index,data)
				
		print '\nLoop finalizado.'
		print '\NEM STANDBY ...'
	print time.sleep(idleTime)
