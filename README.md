# share_wordnet

[![Create Releases](https://github.com/scillidan/share_wordnet/actions/workflows/releases.yml/badge.svg)](https://github.com/scillidan/share_wordnet/actions/workflows/releases.yml)

Data from `Database Packages` on [WordNet](https://wordnet.princeton.edu/download) under [WordNet 3.0 license: (Download)](https://wordnet.princeton.edu/license-and-commercial-use).

## Usage

1. Download files from [Releases](https://github.com/scillidan/share_wordnet/releases).
2. Use them in GoldenDict (StarDict format), sdcv, dictd, Yomichan/Yomitan.
3. See preview screenshot [here](asset/).

### sdcv

```sh
sdcv --color --use-dict WordNet -n <word>
```

### dictd

```sh
# Arch
unzip wordnet-<version>-dictd.zip
sudo cp wordnet-<version>-dictd.{index,dict.dz} /usr/share/dictd/
sudo vim /etc/dict/dictd.conf
```

```
# Add database
database wordnet {
	data /usr/share/dictd/wordnet-*-dictd.dict.dz
	index /usr/share/dictd/wordnet-*-dictd.index
}
```

```sh
sudo systemctl restart dictd.service
```

```sh
dict --host localhost --port 2528 --database wordnet -n <word>
```
