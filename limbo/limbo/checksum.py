import hashlib
from rest_framework.renderers import JSONRenderer
from limbo.serializers import InstrumentSerializer
from limbo.models import Instrument

def setChecksum(instrumentObj):
	serial = InstrumentSerializer(instrumentObj)#, context={'request': request})
	strInstrument = JSONRenderer().render(serial.data)
	checksum = hashlib.sha1(strInstrument).hexdigest()
	instrumentObj.checksum_string = checksum
	instrumentObj.save()
	return checksum
	
def setChecksumAsync(instrPk):
	instrumentObj = Instrument.objects.get(pk=instrPk)
	serial = InstrumentSerializer(instrumentObj)#, context={'request': request})
	strInstrument = JSONRenderer().render(serial.data)
	checksum = hashlib.sha1(strInstrument).hexdigest()
	instrumentObj.checksum_string = checksum
	instrumentObj.save()
	