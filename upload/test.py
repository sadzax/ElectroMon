import sadzax
sadzax.Out.reconfigure_encoding()
sadzax.Out.clear_future_warning()

a = sadzax.Enter.mapped_ints(f'Введите номера файлов')
print(a)
