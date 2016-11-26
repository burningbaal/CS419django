import hashlib
from rest_framework.renderers import JSONRenderer
from limbo.serializers import InstrumentSerializer

def setChecksum(instrumentObj):
	serial = InstrumentSerializer(instrumentObj)#, context={'request': request})
	strInstrument = JSONRenderer().render(serial.data)
	checksum = hashlib.sha1(strInstrument).hexdigest()
	instrumentObj.checksum_string = checksum
	instrumentObj.save()
	return checksum
	
def setChecksumAsync(instrumentObj):
	serial = InstrumentSerializer(instrumentObj)#, context={'request': request})
	strInstrument = JSONRenderer().render(serial.data)
	checksum = hashlib.sha1(strInstrument).hexdigest()
	instrumentObj.checksum_string = checksum
	instrumentObj.save()
	