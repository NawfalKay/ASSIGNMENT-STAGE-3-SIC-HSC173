# Input berupa integer dan float 
angka_bulat = 123
angka_pecahan = 3,14 

# Konversi integer ke string 
angka_bulat_str = str(angka_bulat) 
print(f"Integer: {angka_bulat}, Tipe: {type(angka_bulat)}") 
print(f"String: {angka_bulat_str}, Tipe: {type(angka_bulat_str)}") 

# Konversi float ke string 
angka_pecahan_str = str(angka_pecahan) 
print(f"Float: {angka_pecahan}, Tipe: {type(angka_pecahan)}") 
print(f"String: {angka_pecahan_str}, Tipe: {type(angka_pecahan_str)}")

# Contoh penggabungan string 
pesan = "Nilai integer adalah: " + angka_bulat_str 
print(pesan) 
pesan_desimal = "Nilai float adalah:" + angka_pecahan_str 
print(pesan_desimal)