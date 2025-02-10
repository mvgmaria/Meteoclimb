ccaas = ["Murcia", "Madrid"]

count = len(ccaas)
print(count)
f_str = str(ccaas)[1:-1]
print(f_str)
ff_str = f_str.replace(",", " or region_name =", count - 1)
print(ff_str)
