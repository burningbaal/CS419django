import hashlib

def setChecksum(instrumentObj):
	serial = InstrumentSerializer(instrumentObj)#, context={'request': request})
	strInstrument = strInstrument + JSONRenderer().render(serial.data)
	checksum = hashlib.sha1(strInstrument).hexdigest()
	instrumentObj.checksum_string = checksum
	instrumentObj.Instrument.save()
	