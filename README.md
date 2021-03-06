# RRKDT
## Nearest-neighbor search with $kd$-trees on randomly rotated data

```
@inproceedings{ram2019revisiting,
  title={Revisiting kd-tree for nearest neighbor search},
  author={Ram, Parikshit and Sinha, Kaushik},
  booktitle={Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery \& Data Mining},
  pages={1378--1388},
  year={2019}
}
```



### Installation requirements

This code has been tested on Centos 7 (RHEL 7) and Ubuntu 18.04. The code is designed for `python2.7` because of the [Fast Fast Walsh-Hadamard Transform](https://github.com/FALCONN-LIB/FFHT) library we use for Fast Walsh-Hadamard Transform. We assume the presence of the following:

```
- "Development Tools" (using sudo yum groupinstall "Development Tools" or equivalent)
- epel-release
- python python-devel
- python-pip
- wget

```

Once we have those, we require the following `python2.7` libraries:

```
- numpy
- scipy
- pandas
- matplotlib
- scikit-learn
- tqdm
- h5py
```

In addition, as mentioned earlier, we use the FFHT library for the Fast Walsh-Hadamard Transform. This can be done:

```
wget https://github.com/FALCONN-LIB/FFHT/archive/master.zip
unzip master.zip
cd FFHT-master
pip install . --user
```

OR

```
git clone git@github.com:FALCONN-LIB/FFHT.git
cd FFHT
pip install . --user
```

### Testing the code base

If everything is installed successfully, you can test the working of the code as well as its correctness by executing the following from the root of the library:

```
cd tests
tar -xzvf USPS.tar.gz
cd ..
python2.7 tests/test_all_trees.py
```
