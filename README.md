Espeak installation (preparing for docker)

```
# Install dependencies
RUN apt-get update && apt-get install -y make autoconf automake libtool pkg-config gcc libsonic-dev wget unzip

# Download source
RUN wget https://github.com/espeak-ng/espeak-ng/releases/download/1.49.2/espeak-ng-1.49.2.tar.gz \
    && tar xf espeak-ng-1.49.2.tar.gz \
    && mv espeak-ng-1.49.2 espeak-ng \
    && rm -f espeak-ng-1.49.2.tar.gz

# Chinese ideograms and their Pinyin translations for Mandarin Chinese
RUN wget http://espeak.sourceforge.net/data/zh_listx.zip \
    && unzip zh_listx.zip \
    && mv zh_listx espeak-ng/dictsource/zh_listx \
    && rm -f zh_listx.zip

# Chinese ideograms and their phonetic translations for Cantonese
RUN wget http://espeak.sourceforge.net/data/zhy_list.zip \
    && unzip zhy_list.zip \
    && mv zhy_list espeak-ng/dictsource/zhy_list \
    && rm -f zhy_list.zip

# Additional dictionary information of the Russian words and their stress position
RUN wget http://espeak.sourceforge.net/data/ru_listx.zip \
    && unzip ru_listx.zip \
    && mv ru_listx espeak-ng/dictsource/ru_listx \
    && rm -f ru_listx.zip

# Build and install
RUN cd espeak-ng \
    && ./autogen.sh \
    && ./configure --prefix=/usr --with-mbrola --with-sonic --with-async --with-extdict-ru --with-extdict-zh --with-extdict-zhy \
    && make \
    && make LIBDIR=/usr/lib/x86_64-linux-gnu install

# Download mbrola binary
RUN apt-get install -y mbrola

# <ALTERNATIVE> MBROLA BINARY download, move i386 variant to /usr/bin as "mbrola"
#RUN wget http://www.tcts.fpms.ac.be/synthesis/mbrola/bin/pclinux/mbr301h.zip \
#    && unzip mbr301h.zip \
#    && mv mbrola-linux-i386 /usr/bin/mbrola \
#    && rm -f mbrola* \
#    && rm -f readme.txt \
#    && rm -f mbr301h.zip

# Download and unpack (configured few) mbrola voices (NOTE fr4 uses/requires fr1)
RUN mkdir -p /usr/share/mbrola \
    && wget http://www.tcts.fpms.ac.be/synthesis/mbrola/dba/de3/de3-000307.zip \
    && unzip de3-000307.zip -d /usr/share/mbrola/ \
    && rm -f de3-000307.zip \
    && wget http://www.tcts.fpms.ac.be/synthesis/mbrola/dba/en1/en1-980910.zip \
    && unzip en1-980910.zip -d /usr/share/mbrola/ \
    && rm -f en1-980910.zip \
    && wget http://www.tcts.fpms.ac.be/synthesis/mbrola/dba/sw2/sw2-140102.zip \
    && unzip sw2-140102.zip -d /usr/share/mbrola/ \
    && rm -f sw2-140102.zip \
    && wget http://www.tcts.fpms.ac.be/synthesis/mbrola/dba/us1/us1-980512.zip \
    && unzip us1-980512.zip -d /usr/share/mbrola/ \
    && rm -f us1-980512.zip
```