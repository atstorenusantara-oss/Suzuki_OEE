from pymcprotocol import Type3E

plc = Type3E()
try:
    # Menghubungkan ke PLC
    plc.connect("172.16.134.39", 9000)
    
    # Membaca data dari alamat B0 (sama dengan B000 dalam format Hex)
    # Membaca 5 unit word (masing-masing 16 bit)
    data = plc.batchread_wordunits("D1103",1)
    print(f"Data terbaca (Raw): {data}")
    
    # Konversi data word ke ASCII
    # Setiap Word (16 bit) berisi 2 karakter ASCII (Low byte dan High byte)
    ascii_str = ""
    for word in data:
        char_low = chr(word & 0xFF)
        char_high = chr((word >> 8) & 0xFF)
        ascii_str += char_low + char_high
    
    # Menghilangkan karakter null atau spasi di akhir
    cleaned_str = ascii_str.strip('\x00').strip()
    print(f"Data terbaca (ASCII): {cleaned_str}")

except Exception as e:
    print(f"Gagal terhubung atau membaca dari PLC: {e}")
finally:
    plc.close()
