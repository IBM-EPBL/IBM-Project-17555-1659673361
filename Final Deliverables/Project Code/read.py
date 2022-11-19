import h5py
f = h5py.File('nutrition.h5','r')
f.keys()
for key in f.keys():
    print(key) 
    print(type(f[key]))