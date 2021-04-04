# -*- coding: utf-8 -*-
"""NOMINAL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KnwVtvFQoiRMudKcmATgp5wq7IgBqQsy
"""

from typing import List
import numpy as np

nominal = {'0':'Nol',
           '1':'Satu',
           '2':'Dua',
           '3':'Tiga',
           '4':'Empat',
           '5':'Lima',
           '6':'Enam',
           '7':'Tujuh',
           '8':'Delapan',
           '9':'Sembilan'}

def leading_zero_string(nominal_str:List,limit_leading:int)->List:
    """
    Mengisi subvalue yang tidak berisi 3 elemen dengan memasukkan leading-zero agar menjadi 3 element subvalue.

    Parameter
        nominal_str (List)  : Subvalue List, i.e ['Satu'] -> ['Nol','Nol','Satu']
        limit_leading (int) : batas isian leading zero, i.e 3 berarti subvalue harus berelemen tiga dan kekurangannya diisi oleh leading zero
    Output
        Result (List)       : Leading-zero subvalue, i.e ['Nol','Nol','Satu']
    """
    nominal_copy = nominal_str.copy()
    while len(nominal_copy[0])<limit_leading:
        nominal_copy[0].insert(0,'Nol')
    return nominal_copy

def split_nominal_string(nominal_int:int)->List:
    """
    Mengubah dan membagi nominal menjadi bentu string dengan separasi ribuan (3-sized element chunks).

    Parameter
        nominal_int (int)  : Nominal currency, i.e 25000
    Output
        Result (List)      : Leading-zero subvalue chunks, i.e 1523 -> [['Nol','Nol','Satu'],['Lima','Dua','Tiga']]
    """
    nominal_str = list(str(nominal_int))
    nominal_map = [nominal[k] for k in nominal_str]
    reversed_nominal_map = nominal_map[::-1]
    split_nominal = [reversed_nominal_map[i:i+3] for i in range(0, len(reversed_nominal_map), 3)]
    original_split_nominal = [p[::-1] for p in split_nominal][::-1]
    leading_split_nominal = leading_zero_string(original_split_nominal,3)
    return leading_split_nominal

def tambah_sub_satuan(nominal_str:List)->List:
    """
    Menambah keterangan puluhan atau ratusan untuk setiap 3-sized chunks pada string-nominal.

    Parameter
        nominal_str (List)  : Nominal in string list, i.e [['Nol','Nol','Satu'],['Lima','Dua','Tiga']]
    Output
        Result (List)       : Leading-zero subvalue chunks dengan satuan, i.e 1523 -> [['Nol','Nol','Satu'],['Lima Ratus','Dua Puluh','Tiga']]
    """
    nominal_copy = nominal_str.copy()
    second_num = nominal_copy[1]
    if nominal_copy[0] != 'Nol':
        nominal_copy[0] = 'Seratus' if nominal_copy[0] == 'Satu' else f'{nominal_copy[0]} Ratus'
    if nominal_copy[1] != 'Nol':
        second_num = 'Sepuluh' if nominal_copy[1] == 'Satu' else f'{nominal_copy[1]} Puluh'
    if nominal_copy[1] == 'Satu' and nominal_copy[-1] != 'Nol':
        second_num = 'Sebelas' if nominal_copy[-1] == 'Satu' else f'{nominal_copy[-1]}belas'
        nominal_copy[-1] = 'Nol'
    nominal_copy[1] = second_num  
    return nominal_copy

def tambah_satuan_primer(nominal_str:List)->List:
    """
    Menyesuaikan satuan jutaan atau ribuan pada separasi antar 3-sized chunks.

    Parameter
        nominal_str (List)  : Leading-zero chunks dengan satuan, i.e [['Nol','Nol','Satu'],['Lima Ratus','Dua Puluh','Tiga']]
    Output
        Result (List)       : Leading-zero chunks dengan satuan dalam chunks dan antar chunks, i.e 1523 -> [['Nol','Nol','Seribu'],['Lima Ratus','Dua Puluh','Tiga']],
                                                                                                   2500 -> [['Nol','Nol','Dua Ribu'],['Lima Ratus','Nol','Nol']]
    """
    nominal_length = len(nominal_str)
    nominal_copy = nominal_str.copy()
    if nominal_length == 2:
        if nominal_copy[0] == ['Nol','Nol','Satu']:
            nominal_copy[0][-1] = 'Seribu'
        else:
            nominal_copy[0].append('Ribu')
    elif nominal_length == 3:
        if nominal_copy[1] == ['Nol','Nol','Satu']:
            nominal_copy[1][-1] = 'Seribu'
        else:
            if list(set(nominal_copy[1])) != ['Nol'] and list(set(nominal_copy[-1])) != ['Nol']: 
                nominal_copy[1].append('Ribu')
        nominal_copy[0].append('Juta')
    return nominal_copy

def tambah_satuan(nominal_str:List)->List:
    """
    Mengonversikan bentuk nominal string ke dalam bentuk string yang sesuai.

    Parameter
        nominal_str (List)  : Nominal currency, i.e 1523 -> [['Nol','Nol','Satu'],['Lima','Dua','Tiga']]
    Output
        Result (List)       : Bentuk string dari nominal terkait, i.e 1523 -> Seribu Lima Ratus Dua Puluh Tiga 
    """
    joint_value = []
    for x in nominal_str[::-1]:
        subvalue = tambah_sub_satuan(x)
        joint_value.insert(0,subvalue)
    joint_values = tambah_satuan_primer(joint_value)
    flatten_values = list(np.concatenate(joint_values).flat)
    final_values = flatten_values[0] if len(set(flatten_values)) == 1 else ' '.join([str(elem) for elem in list(filter(lambda x:x != 'Nol',flatten_values))])
    return final_values

def konversi_nominal(nominal_integer:int)->str:
    """
    Fungsi utama konversi nominal integer ke bentuk string (terbilang).

    Parameter
        nominal_int (int)  : Nominal currency, i.e 25000
    Output
        Result (List)      : Nominal terbilang, i.e 25000 -> Dua Puluh Lima Ribu
    """
    value_split = split_nominal_string(nominal_integer)
    value_string = tambah_satuan(value_split)
    return value_string

nominal_uang = [6001000, 6001985, 211232211, 9999, 1000, 1500, 2100, 3549, 100000000, 10000000, 0, 52339, 5, 20, 45, 11, 15, 100, 999, 10119, 99999999]
for i in nominal_uang:
    result = konversi_nominal(i)
    print(f'Nominal {i} Terbilang : {result} Rupiah\n')