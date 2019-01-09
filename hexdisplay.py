import sys

## converting an integer to hex value without '0x'
def intToHex(value):
  return hex(value)[2:].upper()

## converting an integer to a printable char
def intToPrintableChar(value):
  # every value under 32 is not printable -> print a dot instead
  if value < 32:
    return '.'
  else: 
    # return the printable char
    return str(chr(value))

## print something without newline
def write(data):
  sys.stdout.write(str(data))

## perform a linebreak
def linebreak():
  sys.stdout.write('\n')

## fill something with something on the left
def fillLeft(value, minimum, fillWith='0'):
  _value = str(value)
  _fillWith = str(fillWith)
  # if the length of data is too low ...
  if len(_value) < minimum:
    # append the given character to the left side
    _value = ( (minimum - len(_value)) * _fillWith ) + _value
  return _value

## print the head line of hexeditor
def writeHexHead(offsetMinimum):
  # print empty characters for displaying correct gaps
  write(' ' * (offsetMinimum + 4))

  # print every number from 0 to 16 as hex (for byte representation)
  for i in range(0, 16):
    write(fillLeft(intToHex(i), 2) + ' ')

  write(' ')

  # print every number from 0 to 16 as hex (for ascii representation)
  for i in range(0, 16):
    write(fillLeft(intToHex(i), 1))
  
  linebreak()
  linebreak()

## print an offset
def writeOffset(offset, length):
  write('0x' + fillLeft(intToHex(offset), length) + '  ')

## print one line: hex and char values
def writeBufferedBytes(bufferedBytes):
  # print every byte in buffer as hex
  for byte in bufferedBytes:
    write(fillLeft(intToHex(byte),2) + ' ')

  # print empty characters for displaying correct gaps after bytes
  if len(bufferedBytes) < 16:
    write('   ' * (16 - len(bufferedBytes)))
    
  write(' ')

  # print every byte in buffer as ascii
  for byte in bufferedBytes:
    write(intToPrintableChar(byte))

  # print empty characters for displaying correct gaps after ascii
  if len(bufferedBytes) < 16:
    write(' ' * (16 - len(bufferedBytes)))

  write(' ')

  linebreak()

## main function
def main():
  # check commandline parameters
  if len(sys.argv) < 2:
    print('error: please specify filename as commandline parameter')
    quit()
  
  filename = sys.argv[1]

  # read content from given file
  filecontent = None
  with open(filename, 'rb') as fileHandle:
    filecontent = fileHandle.read()

  # convert filecontent to bytes (byte array)
  byteData = bytearray(filecontent)
  
  # define the length of the highest offset
  offsetMinimum = len(intToHex(len(byteData)))
  
  # print the head line
  writeHexHead(offsetMinimum)

  # buffering every line of bytes. print only complete byte lines
  bufferedBytes = []
  for index, byte in enumerate(byteData):
    # appending every byte to buffer
    bufferedBytes.append(byte)

    # write offset and bytes only one line is buffered
    if index % 16 == (16 - 1):
      writeOffset(index - (16 - 1), offsetMinimum)
      writeBufferedBytes(bufferedBytes)

      # clear buffer after print execution
      del bufferedBytes[:] 

  # if the buffer is not empty: write offset and bytes for odd bytes
  if len(bufferedBytes) > 0:
    writeOffset(index - (len(bufferedBytes)-1), offsetMinimum)
    writeBufferedBytes(bufferedBytes)

## application start
if __name__ == '__main__':
  main()