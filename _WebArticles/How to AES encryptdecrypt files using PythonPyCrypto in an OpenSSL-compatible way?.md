# How to AES encrypt/decrypt files using Python/PyCrypto in an OpenSSL-compatible way?


There are many ways to use AES, resulting in frequent incompatibilities between different implementations. OpenSSL provides a popular command line interface for AES encryption/decryption:

    
    
    openssl aes-256-cbc -salt -in filename -out filename.enc
    openssl aes-256-cbc -d -in filename.enc -out filename
    

<strike>This could make for a standard.</strike>

Python has support for AES in the shape of the PyCrypto package, but it only provides the tools. How to use Python/PyCrypto to encrypt files in a way that OpenSSL can be used to decrypt them, and to decrypt files that have been encrypted using OpenSSL?

[python](/questions/tagged/python) [encryption](/questions/tagged/encryption) [openssl](/questions/tagged/openssl) [aes](/questions/tagged/aes) [pycrypto](/questions/tagged/pycrypto)

[share](/q/16761458)|[improve this question](/posts/16761458/edit)

[edited May 30 '13 at 13:21](/posts/16761458/revisions)

asked May 26 '13 at 16:47

![](https://www.gravatar.com/avatar/942f6a63d4a85a1fc660ea6662e85832?s=32&d=identicon&r=PG)

[Thijs van Dien](/users/1163893/thijs-van-dien)

2,8681931

2

 

+1 for following up on yourself, but this wouldn't make a good standard, since password-based key derivation is based on a single iteration of MD5 (though with salt). At the very least, PBKDF2/scrypt should be used with a lot more iterations. - [SquareRootOfTwentyThree](/users/482262/squarerootoftwentythree) May 27 '13 at 13:49

  
 

@SquareRootOfTwentyThree Thanks, I investigated that particular subject a little and good point. - [Thijs van Dien](/users/1163893/thijs-van-dien) May 30 '13 at 13:19

add a comment | 

##  3 Answers 3

[ active](/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible?answertab=active#tab-top) [ oldest](/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible?answertab=oldest#tab-top) [ votes](/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible?answertab=votes#tab-top)

up vote 52 down vote accepted

Given the popularity of Python, at first I was disappointed that there was no complete answer to this question to be found. It took me a fair amount of reading different answers on this board, as well as other resources, to get it right. I thought I might share the result for future reference and perhaps review; I'm by no means a cryptography expert! However, the code below appears to work seamlessly:

    
    
    from hashlib import md5
    from Crypto.Cipher import AES
    from Crypto import Random
    
    def derive_key_and_iv(password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]
    
    def encrypt(in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = Random.new().read(bs - len('Salted__'))
        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out_file.write('Salted__' + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * bs)
            if len(chunk) == 0 or len(chunk) % bs != 0:
                padding_length = (bs - len(chunk) % bs) or bs
                chunk += padding_length * chr(padding_length)
                finished = True
            out_file.write(cipher.encrypt(chunk))
    
    def decrypt(in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = in_file.read(bs)[len('Salted__'):]
        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                chunk = chunk[:-padding_length]
                finished = True
            out_file.write(chunk)
    

Usage:

    
    
    with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
        encrypt(in_file, out_file, password)
    with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
        decrypt(in_file, out_file, password)
    

If you see a chance to improve on this or extend it to be more flexible (e.g. make it work without salt, or provide Python 3 compatibility), please feel free to do so.

## Update

There was a bug in here that caused the last bytes of the original file to be discarded if they happened to have the same value as the padding bytes!

[share](/a/16761459)|[improve this answer](/posts/16761459/edit)

[edited Sep 29 '13 at 16:50](/posts/16761459/revisions)

answered May 26 '13 at 16:47

![](https://www.gravatar.com/avatar/942f6a63d4a85a1fc660ea6662e85832?s=32&d=identicon&r=PG)

[Thijs van Dien](/users/1163893/thijs-van-dien)

2,8681931

  
 

How does this implementation compare to [this one](http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/)? Are there any relative advantages or disadvantages? - [rattray](/users/1048433/rattray) Nov 6 '13 at 3:00

  
 

@rattray The main difference is that your example is one like many others about general use of AES in Python. Mine is all about compatibility with the OpenSSL implementation, so that you can use a well-known command line tool for decryption of files encrypted with the Python code above, and the other way around. - [Thijs van Dien](/users/1163893/thijs-van-dien) Nov 6 '13 at 22:26

  
 

ThijsvanDien and Gregor, you guys, just made my day! Thank you so much! - [Barmaley](/users/2137711/barmaley) Oct 27 '14 at 19:26

1

 

@KennyPowers I don't think you can without breaking OpenSSL compatibility, which was the main goal of this question. If you don't need that, there are better ways to perform encryption that will also give you the flexibility you need. - [Thijs van Dien](/users/1163893/thijs-van-dien) Sep 2 '15 at 0:46

1

 

@SteveWalsh My code expects binary whereas your `file.enc` is base64-encoded (given the `-a` parameter). Drop that parameter or decode the file before decrypting. For further support please start your own question. - [Thijs van Dien](/users/1163893/thijs-van-dien) Mar 3 at 0:52

 |  show **5** more comments

up vote 9 down vote

I am re-posting your code with a couple of corrections (I didn't want to obscure your version). While your code works, it does not detect some errors around padding. In particular, if the decryption key provided is incorrect, your padding logic may do something odd. If you agree with my change, you may update your solution.

    
    
    from hashlib import md5
    from Crypto.Cipher import AES
    from Crypto import Random
    
    def derive_key_and_iv(password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]
    
    def encrypt(in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = Random.new().read(bs - len('Salted__'))
        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out_file.write('Salted__' + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * bs)
            if len(chunk) == 0 or len(chunk) % bs != 0:
                padding_length = bs - (len(chunk) % bs)
                chunk += padding_length * chr(padding_length)
                finished = True
            out_file.write(cipher.encrypt(chunk))
    
    def decrypt(in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = in_file.read(bs)[len('Salted__'):]
        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                if padding_length < 1 or padding_length > bs:
                   raise ValueError("bad decrypt pad (%d)" % padding_length)
                # all the pad-bytes must be the same
                if chunk[-padding_length:] != (padding_length * chr(padding_length)):
                   # this is similar to the bad decrypt:evp_enc.c from openssl program
                   raise ValueError("bad decrypt")
                chunk = chunk[:-padding_length]
                finished = True
            out_file.write(chunk)
    

[share](/a/20457519)|[improve this answer](/posts/20457519/edit)

[edited Dec 10 '13 at 13:13](/posts/20457519/revisions)

answered Dec 8 '13 at 18:54

![](https://www.gravatar.com/avatar/1772a5b36bba7347fb38d344ef897e88?s=32&d=identicon&r=PG)

[Gregor](/users/194034/gregor)

437412

3

 

Please just edit my post. It is peer reviewed anyway. Generally I agree some error checking is good. Though 'missing pad' is kind of misleading when actually there's too much of it. Is that the same error OpenSSL gives? - [Thijs van Dien](/users/1163893/thijs-van-dien) Dec 8 '13 at 19:50

  
 

Corrected to more closely match openssl output from evp_enc.c which outputs the same "bad decrypt" message for both cases. - [Gregor](/users/194034/gregor) Dec 10 '13 at 13:17

  
 

Great! I want to decrypt in .NET too. Can anyone help me convert for this language? - [ECC](/users/1347355/ecc) Jan 14 '14 at 18:54

add a comment | 

up vote 6 down vote

The code below should be Python 3 compatible with the small changes documented in the code. Also wanted to use os.urandom instead of Crypto.Random. 'Salted__' is replaced with salt_header that can be tailored or left empty if needed.

    
    
    from os import urandom
    from hashlib import md5
    
    from Crypto.Cipher import AES
    
    def derive_key_and_iv(password, salt, key_length, iv_length):
        d = d_i = b''  # changed '' to b''
        while len(d) < key_length + iv_length:
            # changed password to str.encode(password)
            d_i = md5(d_i + str.encode(password) + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]
    
    def encrypt(in_file, out_file, password, salt_header='', key_length=32):
        # added salt_header=''
        bs = AES.block_size
        # replaced Crypt.Random with os.urandom
        salt = urandom(bs - len(salt_header))
        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # changed 'Salted__' to str.encode(salt_header)
        out_file.write(str.encode(salt_header) + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * bs) 
            if len(chunk) == 0 or len(chunk) % bs != 0:
                padding_length = (bs - len(chunk) % bs) or bs
                # changed right side to str.encode(...)
                chunk += str.encode(
                    padding_length * chr(padding_length))
                finished = True
            out_file.write(cipher.encrypt(chunk))
    
    def decrypt(in_file, out_file, password, salt_header='', key_length=32):
        # added salt_header=''
        bs = AES.block_size
        # changed 'Salted__' to salt_header
        salt = in_file.read(bs)[len(salt_header):]
        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(
                in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = chunk[-1]  # removed ord(...) as unnecessary
                chunk = chunk[:-padding_length]
                finished = True 
                out_file.write(
                    bytes(x for x in chunk))  # changed chunk to bytes(...)
    

[share](/a/21708946)|[improve this answer](/posts/21708946/edit)

[edited Mar 7 '15 at 17:26](/posts/21708946/revisions)

![](https://www.gravatar.com/avatar/12b88d84c8da1100cf27a691778b419a?s=32&d=identicon&r=PG)

[Stephen J. Fuhry](/users/111033/stephen-j-fuhry)

4,82422944

answered Feb 11 '14 at 17:33

![](https://www.gravatar.com/avatar/58c4de158ad70bbf6473325933ef2419?s=32&d=identicon&r=PG)

[Johnny Booy](/users/3298340/johnny-booy)

6911

  
 

This code was obviously untested and doesn't work as is. - [Chris Arndt](/users/390275/chris-arndt) Sep 2 '14 at 17:01

1

 

@ChrisArndt Works fine for me on python 3. - [Stephen J. Fuhry](/users/111033/stephen-j-fuhry) Mar 7 '15 at 17:15

1

 

Sorry, I don't recall anymore, what wasn't working for me. However, I implemented my own script to encrypt a file with AES: [gist.github.com/SpotlightKid/53e1eb408267315de620](https://gist.github.com/SpotlightKid/53e1eb408267315de620) - [Chris Arndt](/users/390275/chris-arndt) Mar 12 '15 at 12:55

  
 

@ChrisArndt Hello there, I like your script, what if there is no padding in encrypted file? (it throws exception). To generate **perfect** file use `dd if=/dev/zero of=file.txt count=1 bs=1048576` and try encrypting it + decrypting it you should get `ValueError: Bad decrypt pad (0)` - [Kyslik](/users/1564365/kyslik) Oct 18 '15 at 13:24

  
 

@Kyslik I don't quite follow. I answered your comment on my Gist - [Chris Arndt](/users/390275/chris-arndt) Oct 19 '15 at 15:23

 |  show **1** more comment

