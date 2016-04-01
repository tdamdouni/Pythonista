import math, struct, array, sys, time, re

if __name__ == "__main__":
    import wave

    #Comment

    file = wave.open('nat-test-notsure.wav', 'rb')
    samples = array.array('h', file.readframes( file.getnframes()))
    file.close()
    delay_length = int(divmod(44100, 520.5)[0] / 2.0)
    print delay_length
    out_data = ''
    last_val = 0
    zero_counter = 0
    bit_width_ctr = 0
    bitstream = ''
    message = ''
    starttime = time.clock()

    for i in range(0, len(samples) - delay_length):
	#print samples[i + delay_length], samples[i]
	cor_val = (samples[i + delay_length] * samples[i]) / 1073676289.0
	#print cor_val

	if  cor_val > 0.03:
	    zero_counter = 0
	    out_data += struct.pack('<h', 16600)
	    if last_val == -16600:
		bit_width_ctr = 0
	    last_val = 16600

	elif cor_val < -0.03:
	    zero_counter = 0
	    out_data += struct.pack('<h', -16600)
	    if last_val == 16600:
		bit_width_ctr = 0
	    last_val = -16600

	else:
	    zero_counter += 1
	    if zero_counter > 512:
		out_data += struct.pack('<h', 0)
		bit_width_ctr = 0
	    else:
		out_data += struct.pack('h', last_val)
	if cor_val > 0.108: cor_val = 0.108
	if cor_val < -0.108: cor_val = -0.108
	out_data += struct.pack('<h', int(cor_val * 300767))
	bit_width_ctr += 1
	if bit_width_ctr == delay_length:
	    if last_val == -16600:
		bitstream += '0'
	    if last_val == 16600:
		bitstream += '1'
	if bit_width_ctr == (delay_length * 2):
	    bit_width_ctr = 0

    #print bitstream
    msg_collection = re.split(r'11010101', bitstream)
    #print thing_list
    messages = []
    for bits in msg_collection:
	if len(bits) > 7:
	    message = ''
	    for i in range(0, len(bits), 8):
		byte = bits[i:i+8]
		message += chr(int(byte[::-1], 2))
	    if message.startswith(('ZCZC', 'NNNN')):
		messages.append(message)

    print messages
    elapsedtime = (time.clock() - starttime)
    print elapsedtime
    file = wave.open('correlated.wav', 'wb')
    file.setparams( (2, 2, 44100, 44100, 'NONE', '') )
    file.writeframes(out_data)
    file.close()

